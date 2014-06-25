from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import RequestContext
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from models import OTItem, OTItemDelivery, OTItemReturn, OTItemStorage, OTItemUsage,OTItemDaily
from django.db.models import Sum


from django.http import HttpResponse
from django.shortcuts import render_to_response, render, HttpResponseRedirect, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.forms.models import model_to_dict

from forms import LoginForm, SignupForm

#rest framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

import logging
logger = logging.getLogger(__name__)



def main_view(request):
    user = request.user
    if user.is_anonymous() or not user.is_authenticated:
        return redirect('/login/')
    else:
        return redirect('/member')

def login_view(request):
    #default to member page
    next = '/member/'
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user and user.is_active:
                #do the real login
                login(request, user)
            #redirect
            return HttpResponseRedirect(request.POST.get('next'))
        else:
            print 'invalid login'
    else:
        form = LoginForm()
        if request.method == 'GET' and 'next' in request.GET:
            next = request.GET.get('next')
    return render(request, "registration/login.html", {
        'form': form,
        'next': next
    })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

def register_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            #we need to
            if new_user and new_user.is_active:
                #do the real login
                login(request, new_user)
            #redirect to the next page
            return HttpResponseRedirect('/member/')
        else:
            print 'invalid'
    else:
        form = SignupForm()
    return render(request, "registration/register.html", {
        'form': form,
    })

def member_view(request):
    dict = {}
    return render_to_response('website/day.html', RequestContext(request, dict))

def usage_report_view(request):
    usage_list = OTItemDaily.objects.select_related('OTItem').filter(type=OTItemDaily.type_usage).order_by('date')
    print usage_list
    dict = {'usage_list':usage_list}
    return render_to_response('website/usage-report.html', RequestContext(request, dict))

def return_report_view(request):
    return_list = OTItemDaily.objects.select_related('OTItem').filter(type=OTItemDaily.type_return).order_by('date')
    print return_list
    dict = {'return_list':return_list}
    return render_to_response('website/return-report.html', RequestContext(request, dict))

def delivery_report_view(request):
    delivery_list = OTItemDaily.objects.select_related('OTItem').filter(type=OTItemDaily.type_delivery).order_by('date')
    print delivery_list.query
    dict = {'delivery_list':delivery_list}
    return render_to_response('website/delivery-report.html', RequestContext(request, dict))

def summary_report_view(request):

    inventory_list = OTItemDaily.objects.values('OTItem').annotate(sum = Sum('amount'))


    print inventory_list.query
    dict = {'inventory_list':inventory_list}
    return render_to_response('website/summary-report.html', RequestContext(request, dict))


# ------------------------------------------------- #
# RESTful APIs and its Utilities
# ------------------------------------------------- #

class OperationCode:
    DELIVERY, RETURN, USAGE = range(3)

def __is_user_authorized(user):
    if user.is_anonymous() or not user.is_authenticated:
        return False
    else:
        return True

def __handle_item_add(date, item_id, oid, user, amount):
    d = None
    if oid == OperationCode.DELIVERY:
        d, created = OTItemDelivery.objects.get_or_create(item_id=item_id, amount=amount)
    elif oid == OperationCode.RETURN:
        d,created = OTItemReturn.objects.get_or_create(item_id=item_id, amount=amount)
    elif oid == OperationCode.USAGE:
        d, created = OTItemUsage.objects.get_or_create(item_id=item_id, amount=amount)
    return d

def __handle_item_update(id, item_id, oid, user, amount):
    d = None
    if oid == OperationCode.DELIVERY:
        d = OTItemDelivery.objects.get(id=id)
    elif oid == OperationCode.RETURN:
        d = OTItemReturn.objects.get(id=id)
    elif oid == OperationCode.USAGE:
        d = OTItemUsage.objects.get(id=id)
    d.item_id = item_id
    d.amount = amount
    d.save()
    return d

def __handle_item_remove(id, oid):
    if oid == OperationCode.DELIVERY:
        d = OTItemDelivery.objects.get(id=id)
    elif oid == OperationCode.RETURN:
        d = OTItemReturn.objects.get(id=id)
    elif oid == OperationCode.USAGE:
        d = OTItemUsage.objects.get(id=id)
    d.delete()

@api_view(['POST'])
def add_handler(request, oid):
    print request.DATA
    user = request.user
    if __is_user_authorized(user):
        date = request.DATA.get('date', None)
        item_id = request.DATA.get('item_id', None)
        amount = int(request.DATA.get('amount', 0))
        if item_id and date:
            new_record = __handle_item_add(date, item_id, user, amount)
            results = model_to_dict(new_record)
            return Response(results, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def update_handler(request, oid):
    print request.DATA
    user = request.user
    if __is_user_authorized(user):
        record_id = request.DATA.get('record_id', None)
        item_id = request.DATA.get('item_id', None)
        amount = int(request.DATA.get('amount', 0))
        if item_id and record_id:
            new_record = __handle_item_update(record_id, item_id, item_id, user, amount)
            results = model_to_dict(new_record)
            return Response(results, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def remove_handler(request, oid):
    print request.DATA
    user = request.user
    if __is_user_authorized(user):
        record_id = request.DATA.get('record_id', None)
        if record_id:
            __handle_item_remove(record_id, oid)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)



