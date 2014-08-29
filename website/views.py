# -*- coding: utf-8 -*-
# coding=gbk1
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from models import OTItem, OTItemDaily, OTItemMonthly

from django.shortcuts import render_to_response, render, HttpResponseRedirect, redirect
from django.contrib.auth import logout, login
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
logging.basicConfig(level=logging.DEBUG)

from serializers import OTItemDailySerializer

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
    context_dict = {}
    return render_to_response('website/day.html', RequestContext(request, context_dict))

@login_required
def usage_report_view(request):

    p = request.GET.get('dimension')
    start_date = request.GET.get('startDate');
    end_date = request.GET.get('endDate');
    part_no = request.GET.get('part-no');
    export_excel = request.GET.get("export-excel");
    print start_date,end_date,part_no

    if p == 'day':
        usage_list = OTItemDaily.objects.select_related('OTItem').filter(type=OTItemDaily.type_usage).order_by('-date','OTItem__item_no')
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

        if export_excel is not None and export_excel.upper() == 'TRUE':
            response = render_to_response("website/daily-spreadsheet.html", {
                'daily_list': usage_list,
            })
            filename = "usage-daily-spreadsheet.xls"
            response['Content-Disposition'] = 'attachment; filename='+filename
            response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'
            return response
        else:
            paginator = Paginator(usage_list,50)
            page = request.GET.get('page')
            try:
                usages = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                usages = paginator.page(1)
            except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
                usages = paginator.page(paginator.num_pages)
            context_dict = {'daily_list':usages,
                    'title': '使用情况'}
            return render_to_response('website/report.html', RequestContext(request, context_dict))
    elif p == 'month':
        usage_list = OTItemMonthly.objects.select_related('OTItem').filter(type=OTItemMonthly.type_usage).order_by('-date','OTItem__item_no')
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

        if export_excel is not None and export_excel.upper() == 'TRUE':
            response = render_to_response("website/monthly-spreadsheet.html", {
                'monthly_list': usage_list,
            })
            filename = "usage-monthly-spreadsheet.xls"
            response['Content-Disposition'] = 'attachment; filename='+filename
            response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'
            return response
        else:
            paginator = Paginator(usage_list,50)
            page = request.GET.get('page')
            try:
                usages = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                usages = paginator.page(1)
            except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
                usages = paginator.page(paginator.num_pages)

            context_dict = {'monthly_list':usages,
                    'title': '使用情况'}
            return render_to_response('website/report.html', RequestContext(request, context_dict))
    else :
        first_day_of_current_month = date.today().replace(day=1)
        first_day_of_second_month = first_day_of_current_month - relativedelta(months=1)
        first_day_of_third_month = first_day_of_current_month - relativedelta(months=2)
        params = [first_day_of_third_month.strftime("%Y-%m-%d"),first_day_of_current_month.strftime("%Y-%m-%d"),first_day_of_second_month.strftime("%Y-%m-%d"),first_day_of_third_month.strftime("%Y-%m-%d")]
        print params
        result = get_sql_data_params(Sql.monthly_usage_sql,params)
        #store the summation of every column
        sum_dict = dict()
        sum_of_history_sum = 0
        sum_of_current_month_sum = 0
        sum_of_second_month_sum = 0
        sum_of_third_month_sum = 0
        for i, val in enumerate(result):
            print val
            sum_of_history_sum += val.get('history_sum',0)
            sum_of_current_month_sum += val.get('current_month_sum',0)
            sum_of_second_month_sum += val.get('second_month_sum',0)
            sum_of_third_month_sum += val.get('third_month_sum',0)
        sum_dict['sum_of_history_sum'] = sum_of_history_sum
        sum_dict['sum_of_current_month_sum'] = sum_of_current_month_sum
        sum_dict['sum_of_second_month_sum'] = sum_of_second_month_sum
        sum_dict['sum_of_third_month_sum'] = sum_of_third_month_sum

        if export_excel is not None and export_excel.upper() == 'TRUE':
            for i, val in enumerate(result):
                str_val = "size: " + val.get("size")
                val.update({"size":str_val})
            context_dict = {'summary_list': result,
            'current_month':first_day_of_current_month.strftime("%Y年%m月"),
            'second_month':first_day_of_second_month.strftime("%Y年%m月"),
            'third_month':first_day_of_third_month.strftime("%Y年%m月"),
            'sum_dict':sum_dict}
            response = render_to_response("website/summary-spreadsheet.html", context_dict)
            filename = "usage-summary-spreadsheet.xls"
            response['Content-Disposition'] = 'attachment; filename='+filename
            response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'
            return response
        else :
            context_dict = {'summary_list': result,
            'current_month':first_day_of_current_month.strftime("%Y年%m月"),
            'second_month':first_day_of_second_month.strftime("%Y年%m月"),
            'third_month':first_day_of_third_month.strftime("%Y年%m月"),
            'sum_dict':sum_dict,
            'title': '使用情况'}
            return render_to_response('website/report.html', RequestContext(request, context_dict))

@login_required
def return_report_view(request):
    p = request.GET.get('dimension')
    start_date = request.GET.get('startDate');
    end_date = request.GET.get('endDate');
    part_no = request.GET.get('part-no');
    export_excel = request.GET.get("export-excel");
    print start_date,end_date,part_no

    if p == 'day':
        return_list = OTItemDaily.objects.select_related('OTItem').filter(type=OTItemDaily.type_return).order_by('-date','OTItem__item_no')
        if start_date is not None:
            tmp = datetime.strptime(start_date,'%m/%d/%Y')
            start_date = tmp.strftime('%Y-%m-%d')
            return_list = return_list.filter(date__gte=start_date)
        if end_date is not None:
            tmp = datetime.strptime(end_date,'%m/%d/%Y')
            end_date = tmp.strftime('%Y-%m-%d')
            return_list = return_list.filter(date__lte=end_date)
        if part_no is not None:
            return_list = return_list.filter(OTItem__part_no__contains=part_no)

        if export_excel is not None and export_excel.upper() == 'TRUE':
            response = render_to_response("website/daily-spreadsheet.html", {
                'daily_list': return_list,
            })
            filename = "return-daily-spreadsheet.xls"
            response['Content-Disposition'] = 'attachment; filename='+filename
            response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'
            return response
        else:
            paginator = Paginator(return_list,50)
            page = request.GET.get('page')
            try:
                returns = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                returns = paginator.page(1)
            except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
                returns = paginator.page(paginator.num_pages)
            context_dict = {'daily_list':returns,
                    'title': '退货情况'}
            return render_to_response('website/report.html', RequestContext(request, context_dict))
    elif p == 'month':
        return_list = OTItemMonthly.objects.select_related('OTItem').filter(type=OTItemMonthly.type_return).order_by('-date','OTItem__item_no')
        if start_date is not None:
            tmp = datetime.strptime(start_date,'%m/%d/%Y')
            tmp = tmp.replace(day=1)
            start_date = tmp.strftime('%Y-%m-%d')
            print start_date
            return_list = return_list.filter(date__gte=start_date)
        if end_date is not None:
            tmp = datetime.strptime(end_date,'%m/%d/%Y')
            tmp = tmp.replace(day=1)
            end_date = tmp.strftime('%Y-%m-%d')
            print end_date
            return_list = return_list.filter(date__lte=end_date)
        if part_no is not None:
            return_list = return_list.filter(OTItem__part_no__contains=part_no)

        if export_excel is not None and export_excel.upper() == 'TRUE':
            response = render_to_response("website/monthly-spreadsheet.html", {
                'monthly_list': return_list,
            })
            filename = "return-monthly-spreadsheet.xls"
            response['Content-Disposition'] = 'attachment; filename='+filename
            response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'
            return response
        else:
            paginator = Paginator(return_list,50)
            page = request.GET.get('page')
            try:
                returns = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                returns = paginator.page(1)
            except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
                returns = paginator.page(paginator.num_pages)
            context_dict = {'monthly_list':returns,
                    'title': '退货情况'}
            return render_to_response('website/report.html', RequestContext(request, context_dict))
    else :
        first_day_of_current_month = date.today().replace(day=1)
        first_day_of_second_month = first_day_of_current_month - relativedelta(months=1)
        first_day_of_third_month = first_day_of_current_month - relativedelta(months=2)
        params = [first_day_of_third_month.strftime("%Y-%m-%d"),first_day_of_current_month.strftime("%Y-%m-%d"),first_day_of_second_month.strftime("%Y-%m-%d"),first_day_of_third_month.strftime("%Y-%m-%d")]
        print params
        result = get_sql_data_params(Sql.monthly_return_sql,params)
        #store the summation of every column
        sum_dict = dict()
        sum_of_history_sum = 0
        sum_of_current_month_sum = 0
        sum_of_second_month_sum = 0
        sum_of_third_month_sum = 0
        for i, val in enumerate(result):
            print val
            sum_of_history_sum += val.get('history_sum',0)
            sum_of_current_month_sum += val.get('current_month_sum',0)
            sum_of_second_month_sum += val.get('second_month_sum',0)
            sum_of_third_month_sum += val.get('third_month_sum',0)
        sum_dict['sum_of_history_sum'] = sum_of_history_sum
        sum_dict['sum_of_current_month_sum'] = sum_of_current_month_sum
        sum_dict['sum_of_second_month_sum'] = sum_of_second_month_sum
        sum_dict['sum_of_third_month_sum'] = sum_of_third_month_sum

        if export_excel is not None and export_excel.upper() == 'TRUE':
            for i, val in enumerate(result):
                str_val = "size: " + val.get("size")
                val.update({"size":str_val})
            context_dict = {'summary_list': result,
            'current_month':first_day_of_current_month.strftime("%Y年%m月"),
            'second_month':first_day_of_second_month.strftime("%Y年%m月"),
            'third_month':first_day_of_third_month.strftime("%Y年%m月"),
            'sum_dict':sum_dict}
            response = render_to_response("website/summary-spreadsheet.html", context_dict)
            filename = "return-summary-spreadsheet.xls"
            response['Content-Disposition'] = 'attachment; filename='+filename
            response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'
            return response
        else :
            context_dict = {'summary_list': result,
            'current_month':first_day_of_current_month.strftime("%Y年%m月"),
            'second_month':first_day_of_second_month.strftime("%Y年%m月"),
            'third_month':first_day_of_third_month.strftime("%Y年%m月"),
            'sum_dict':sum_dict,
            'title': '退货情况'}

            return render_to_response('website/report.html', RequestContext(request, context_dict))

@login_required
def delivery_report_view(request):
    p = request.GET.get('dimension')
    start_date = request.GET.get('startDate');
    end_date = request.GET.get('endDate');
    part_no = request.GET.get('part-no');
    export_excel = request.GET.get("export-excel");

    print start_date,end_date,part_no

    if p == 'day':
        delivery_list = OTItemDaily.objects.select_related('OTItem').filter(type=OTItemDaily.type_delivery).order_by('-date','OTItem__item_no')
        if start_date is not None:
            tmp = datetime.strptime(start_date,'%m/%d/%Y')
            start_date = tmp.strftime('%Y-%m-%d')
            delivery_list = delivery_list.filter(date__gte=start_date)
        if end_date is not None:
            tmp = datetime.strptime(end_date,'%m/%d/%Y')
            end_date = tmp.strftime('%Y-%m-%d')
            delivery_list = delivery_list.filter(date__lte=end_date)
        if part_no is not None:
            delivery_list = delivery_list.filter(OTItem__part_no__contains=part_no)

        if export_excel is not None and export_excel.upper() == 'TRUE':
            response = render_to_response("website/daily-spreadsheet.html", {
                'daily_list': delivery_list,
            })
            filename = "delivery-daily-spreadsheet.xls"
            response['Content-Disposition'] = 'attachment; filename='+filename
            response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'
            return response
        else:
            paginator = Paginator(delivery_list,50)
            page = request.GET.get('page')
            try:
                deliveries = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                deliveries = paginator.page(1)
            except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
                deliveries = paginator.page(paginator.num_pages)
            context_dict = {'daily_list':deliveries,
                    'title': '发货情况'}
            return render_to_response('website/report.html', RequestContext(request, context_dict))
    elif p == 'month':
        delivery_list = OTItemMonthly.objects.select_related('OTItem').filter(type=OTItemMonthly.type_delivery).order_by('-date','OTItem__item_no')
        if start_date is not None:
            tmp = datetime.strptime(start_date,'%m/%d/%Y')
            tmp = tmp.replace(day=1)
            start_date = tmp.strftime('%Y-%m-%d')
            print start_date
            delivery_list = delivery_list.filter(date__gte=start_date)
        if end_date is not None:
            tmp = datetime.strptime(end_date,'%m/%d/%Y')
            tmp = tmp.replace(day=1)
            end_date = tmp.strftime('%Y-%m-%d')
            print end_date
            delivery_list = delivery_list.filter(date__lte=end_date)
        if part_no is not None:
            delivery_list = delivery_list.filter(OTItem__part_no__contains=part_no)

        if export_excel is not None and export_excel.upper() == 'TRUE':
            response = render_to_response("website/monthly-spreadsheet.html", {
                'monthly_list': delivery_list,
            })
            filename = "delivery-monthly-spreadsheet.xls"
            response['Content-Disposition'] = 'attachment; filename='+filename
            response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'
            return response
        else:
            paginator = Paginator(delivery_list,50)
            page = request.GET.get('page')
            try:
                deliveries = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                deliveries = paginator.page(1)
            except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
                deliveries = paginator.page(paginator.num_pages)
            context_dict = {'monthly_list':deliveries,
                    'title': '发货情况'}
            return render_to_response('website/report.html', RequestContext(request, context_dict))
    else :
        first_day_of_current_month = date.today().replace(day=1)
        first_day_of_second_month = first_day_of_current_month - relativedelta(months=1)
        first_day_of_third_month = first_day_of_current_month - relativedelta(months=2)
        params = [first_day_of_third_month.strftime("%Y-%m-%d"),first_day_of_current_month.strftime("%Y-%m-%d"),first_day_of_second_month.strftime("%Y-%m-%d"),first_day_of_third_month.strftime("%Y-%m-%d")]
        result = get_sql_data_params(Sql.monthly_delivery_sql,params)
        #store the summation of every column
        sum_dict = dict()
        sum_of_history_sum = 0
        sum_of_current_month_sum = 0
        sum_of_second_month_sum = 0
        sum_of_third_month_sum = 0
        for i, val in enumerate(result):
            print val
            sum_of_history_sum += val.get('history_sum',0)
            sum_of_current_month_sum += val.get('current_month_sum',0)
            sum_of_second_month_sum += val.get('second_month_sum',0)
            sum_of_third_month_sum += val.get('third_month_sum',0)
        sum_dict['sum_of_history_sum'] = sum_of_history_sum
        sum_dict['sum_of_current_month_sum'] = sum_of_current_month_sum
        sum_dict['sum_of_second_month_sum'] = sum_of_second_month_sum
        sum_dict['sum_of_third_month_sum'] = sum_of_third_month_sum

        if export_excel is not None and export_excel.upper() == 'TRUE':
            for i, val in enumerate(result):
                str_val = "size: " + val.get("size")
                val.update({"size":str_val})
            context_dict = {'summary_list': result,
            'current_month':first_day_of_current_month.strftime("%Y年%m月"),
            'second_month':first_day_of_second_month.strftime("%Y年%m月"),
            'third_month':first_day_of_third_month.strftime("%Y年%m月"),
            'sum_dict':sum_dict}

            response = render_to_response("website/summary-spreadsheet.html", context_dict)
            filename = "delivery-summary-spreadsheet.xls"
            response['Content-Disposition'] = 'attachment; filename='+filename
            response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'
            return response
        else :
            context_dict = {'summary_list': result,
            'current_month':first_day_of_current_month.strftime("%Y年%m月"),
            'second_month':first_day_of_second_month.strftime("%Y年%m月"),
            'third_month':first_day_of_third_month.strftime("%Y年%m月"),
            'sum_dict':sum_dict,
            'title': '发货情况'}
            return render_to_response('website/report.html', RequestContext(request, context_dict))

@login_required
def summary_report_view(request):
    export_excel = request.GET.get("export-excel");

    inventory_list = get_sql_data(Sql.summary_sql)
    # store the summation of every column
    sum_dict = dict()
    sum_of_consignment_amount = 0
    sum_of_delivery_sum = 0
    sum_of_return_sum = 0
    sum_of_usage_sum = 0
    sum_of_total_sum = 0
    sum_of_supplement = 0

    for i, val in enumerate(inventory_list):

        total_sum = val.get("delivery_sum") - val.get("return_sum") - val.get("usage_sum")
        val.update({"total_sum":total_sum})
        supplement = val.get("consignment_amount") - total_sum
        val.update({"supplement":supplement})
        sum_of_consignment_amount += val.get("consignment_amount",0)
        sum_of_delivery_sum += val.get('delivery_sum', 0)
        sum_of_return_sum += val.get('return_sum', 0)
        sum_of_usage_sum += val.get('usage_sum', 0)
        sum_of_total_sum += total_sum
        if supplement > 0:
            sum_of_supplement += supplement

    sum_dict['sum_of_consignment_amount'] = sum_of_consignment_amount
    sum_dict['sum_of_delivery_sum'] = sum_of_delivery_sum
    sum_dict['sum_of_return_sum'] = sum_of_return_sum
    sum_dict['sum_of_usage_sum'] = sum_of_usage_sum
    sum_dict['sum_of_total_sum'] = sum_of_total_sum
    sum_dict['sum_of_supplement'] = sum_of_supplement

    if export_excel is not None and export_excel.upper() == 'TRUE':
            for i, val in enumerate(inventory_list):
                str_val = "size: " + val.get("size")
                val.update({"size":str_val})
            context_dict = {'inventory_list':inventory_list,'sum_dict':sum_dict}

            response = render_to_response("website/summary-report-spreadsheet.html", context_dict)
            filename = "summary-report-spreadsheet.xls"
            response['Content-Disposition'] = 'attachment; filename='+filename
            response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'
            return response
    else :
        context_dict = {'inventory_list':inventory_list,'sum_dict':sum_dict}
        return render_to_response('website/summary-report.html', RequestContext(request, context_dict))

@login_required
def products_view(request):
    products_list = OTItem.objects.select_related('OTDIStandard').order_by('item_no')
    context_dict = {'products_list':products_list}
    return render_to_response('website/products.html', RequestContext(request, context_dict))



# ------------------------------------------------- #
# RESTful APIs and its Utilities
# ------------------------------------------------- #

class OperationCode:
    DELIVERY = "DELIVERY"
    RETURN = "RETURN"
    USAGE = "USAGE"

def __is_user_authorized(user):
    if user.is_anonymous() or not user.is_authenticated:
        return False
    else:
        return True

def __handle_item_add(date, part_no, amount, type):
    d = None
    created= None
    item = OTItem.objects.get(part_no=part_no)
    if item:
        try:
            if type.upper() == OperationCode.DELIVERY:
                d, created = OTItemDaily.objects.get_or_create(OTItem=item, amount=amount, type=OTItemDaily.type_delivery,date=date)
            elif type.upper() == OperationCode.RETURN:
                print type.upper()
                d, created = OTItemDaily.objects.get_or_create(OTItem=item, amount=amount, type=OTItemDaily.type_return,date=date)
            elif type.upper() == OperationCode.USAGE:
                d, created = OTItemDaily.objects.get_or_create(OTItem=item, amount=amount, type=OTItemDaily.type_usage,date=date)
        except Exception as e:
            logger.exception('%s' % e.message)

    logger.debug(d)
    logger.debug(created)
    return d

def __handle_item_update(date, part_no, amount, type):
    d = None
    if type.upper() == OperationCode.DELIVERY:
        d = OTItemDaily.objects.get(OTItem__part_no=part_no,date=date,type=OTItemDaily.type_delivery)
    elif type.upper() == OperationCode.RETURN:
        d = OTItemDaily.objects.get(OTItem__part_no=part_no,date=date,type=OTItemDaily.type_return)
    elif type.upper() == OperationCode.USAGE:
        d = OTItemDaily.objects.get(OTItem__part_no=part_no,date=date,type=OTItemDaily.type_usage)
    if d :
        d.amount = amount
        d.save()
    return d

def __handle_item_remove(date, part_no, type):
    if type.upper() == OperationCode.DELIVERY:
        d = OTItemDaily.objects.get(OTItem__part_no=part_no,date=date,type=OTItemDaily.type_delivery)
    elif type.upper() == OperationCode.RETURN:
        d = OTItemDaily.objects.get(OTItem__part_no=part_no,date=date,type=OTItemDaily.type_return)
    elif type.upper() == OperationCode.USAGE:
        d = OTItemDaily.objects.get(OTItem__part_no=part_no,date=date,type=OTItemDaily.type_usage)
    if d:
        d.delete()

@api_view(['POST'])
def add_handler(request):
    print request.DATA
    user = request.user
    if __is_user_authorized(user):
        date = request.DATA.get('date', None)
        part_no = request.DATA.get('part_no', None)
        type = request.DATA.get('type', None)
        amount = int(request.DATA.get('amount', 0))
        if part_no and date and amount >0 and type:
            date = datetime.strptime(date,'%m/%d/%Y')
            new_record = __handle_item_add(date, part_no, amount, type)
            if new_record:
                results = model_to_dict(new_record)
                return Response(results, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def update_handler(request):
    print request.DATA
    user = request.user
    if __is_user_authorized(user):
        date = request.DATA.get('date', None)
        part_no = request.DATA.get('part_no', None)
        type = request.DATA.get('type', None)
        amount = int(request.DATA.get('amount', 0))
        if date and part_no and amount >0 and type:
            date = datetime.strptime(date,'%m/%d/%Y')
            new_record = __handle_item_update(date, part_no, amount, type)
            if new_record:
                results = model_to_dict(new_record)
                return Response(results, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def remove_handler(request):
    print request.DATA
    user = request.user
    if __is_user_authorized(user):
        date = request.DATA.get('date', None)
        part_no = request.DATA.get('part_no', None)
        type = request.DATA.get('type', None)
        if date and part_no and type:
            date = datetime.strptime(date,'%m/%d/%Y')
            __handle_item_remove(date, part_no, type)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_handler(request):
    print request.GET
    date = request.GET.get('date');
    part_no = request.GET.get('part-no');
    user = request.user
    if __is_user_authorized(user) is False:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    if date is None or part_no is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    tmp = datetime.strptime(date,'%m/%d/%Y')
    start_date = tmp.strftime('%Y-%m-%d')
    records = OTItemDaily.objects.filter(date=start_date,OTItem__part_no=part_no)
    serializer = OTItemDailySerializer(records,many=True)
    return Response(serializer.data)

