# -*- coding: utf-8 -*-
# coding=gbk1
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import RequestContext
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from models import OTItem,  OTItemStorage, OTItemDaily, OTItemMonthly
from django.db.models import Sum



from django.http import HttpResponse
from django.shortcuts import render_to_response, render, HttpResponseRedirect, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.forms.models import model_to_dict

from forms import LoginForm, SignupForm

from utils import get_sql_data,get_sql_data_params
from sql import Sql

from datetime import date,datetime
from dateutil.relativedelta import relativedelta

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
    return HttpResponseRedirect('/login/')

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

@login_required
def member_view(request):
    dict = {}
    return render_to_response('website/day.html', RequestContext(request, dict))

@login_required
def usage_report_view(request):

    p = request.GET.get('dimension')
    start_date = request.GET.get('startDate');
    end_date = request.GET.get('endDate');
    part_no = request.GET.get('part-no');

    print start_date,end_date,part_no

    if p == 'day':
        usage_list = OTItemDaily.objects.select_related('OTItem').filter(type=OTItemDaily.type_usage).order_by('date')
        if start_date is not None:
            tmp = datetime.strptime(start_date,'%m/%d/%Y')
            start_date = tmp.strftime('%Y-%m-%d')
            usage_list = usage_list.filter(date__gte=start_date)
        if end_date is not None:
            tmp = datetime.strptime(end_date,'%m/%d/%Y')
            end_date = tmp.strftime('%Y-%m-%d')
            usage_list = usage_list.filter(date__lte=end_date)
        if part_no is not None:
            usage_list = usage_list.filter(OTItem__part_no__contains=part_no)
        print usage_list
        dict = {'daily_usage_list':usage_list}
        return render_to_response('website/usage-report.html', RequestContext(request, dict))
    elif p == 'month':
        usage_list = OTItemMonthly.objects.select_related('OTItem').filter(type=OTItemMonthly.type_usage).order_by('date')
        if start_date is not None:
            tmp = datetime.strptime(start_date,'%m/%d/%Y')
            tmp = tmp.replace(day=1)
            start_date = tmp.strftime('%Y-%m-%d')
            print start_date
            usage_list = usage_list.filter(date__gte=start_date)
        if end_date is not None:
            tmp = datetime.strptime(end_date,'%m/%d/%Y')
            tmp = tmp.replace(day=1)
            end_date = tmp.strftime('%Y-%m-%d')
            print end_date
            usage_list = usage_list.filter(date__lte=end_date)
        if part_no is not None:
            usage_list = usage_list.filter(OTItem__part_no__contains=part_no)
        print usage_list
        dict = {'monthly_usage_list':usage_list}
        return render_to_response('website/usage-report.html', RequestContext(request, dict))
    else :
        first_day_of_current_month = date.today().replace(day=1)
        first_day_of_second_month = first_day_of_current_month - relativedelta(months=1)
        first_day_of_third_month = first_day_of_current_month - relativedelta(months=2)
        params = [first_day_of_current_month.strftime("%Y-%m-%d"),first_day_of_second_month.strftime("%Y-%m-%d"),first_day_of_third_month.strftime("%Y-%m-%d")]
        print params
        result = get_sql_data_params(Sql.monthly_usage_sql,params)

        dict = {'summary_usage_list': result,
            'current_month':first_day_of_current_month.strftime("%Y年%m月"),
            'second_month':first_day_of_second_month.strftime("%Y年%m月"),
            'third_month':first_day_of_third_month.strftime("%Y年%m月")}
        return render_to_response('website/usage-report.html', RequestContext(request, dict))

@login_required
def return_report_view(request):
    return_list = OTItemDaily.objects.select_related('OTItem').filter(type=OTItemDaily.type_return).order_by('date')
    print return_list
    dict = {'return_list':return_list}
    return render_to_response('website/return-report.html', RequestContext(request, dict))
@login_required
def delivery_report_view(request):
    delivery_list = OTItemDaily.objects.select_related('OTItem').filter(type=OTItemDaily.type_delivery).order_by('date')
    print delivery_list.query
    dict = {'delivery_list':delivery_list}
    return render_to_response('website/delivery-report.html', RequestContext(request, dict))
@login_required
def summary_report_view(request):

    #inventory_list = OTItemDaily.objects.values('OTItem').annotate(sum = Sum('amount'))
    inventory_list = get_sql_data(Sql.summary_sql)
    for i, val in enumerate(inventory_list):

        total_sum = val.get("delivery_sum") - val.get("return_sum") - val.get("usage_sum")
        val.update({"total_sum":total_sum})
        supplement = val.get("consignment_amount") - total_sum
        if val.get("consignment_amount") - total_sum < 0:
            supplement = 0;
        val.update({"supplement":supplement})
        print i, val
    dict = {'inventory_list':inventory_list}
    return render_to_response('website/summary-report.html', RequestContext(request, dict))

@login_required
def products_view(request):
    products_list = OTItem.objects.all()
    dict = {'products_list':products_list}
    return render_to_response('website/products.html', RequestContext(request, dict))



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
        d, created = OTItemDaily.objects.get_or_create(item_id=item_id, amount=amount)
    elif oid == OperationCode.RETURN:
        d,created = OTItemDaily.objects.get_or_create(item_id=item_id, amount=amount)
    elif oid == OperationCode.USAGE:
        d, created = OTItemDaily.objects.get_or_create(item_id=item_id, amount=amount)
    return d

def __handle_item_update(id, item_id, oid, user, amount):
    d = None
    if oid == OperationCode.DELIVERY:
        d = OTItemDaily.objects.get(id=id)
    elif oid == OperationCode.RETURN:
        d = OTItemDaily.objects.get(id=id)
    elif oid == OperationCode.USAGE:
        d = OTItemDaily.objects.get(id=id)
    d.item_id = item_id
    d.amount = amount
    d.save()
    return d

def __handle_item_remove(id, oid):
    if oid == OperationCode.DELIVERY:
        d = OTItemDaily.objects.get(id=id)
    elif oid == OperationCode.RETURN:
        d = OTItemDaily.objects.get(id=id)
    elif oid == OperationCode.USAGE:
        d = OTItemDaily.objects.get(id=id)
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



