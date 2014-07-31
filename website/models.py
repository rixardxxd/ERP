# -*- coding: utf-8 -*-
# coding=gbk
from django.db import models
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.template import defaultfilters
from datetime import date
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class Consignment(models.Model):

    class Meta:
        verbose_name = "寄卖数量表"


    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveIntegerField(default=0,verbose_name="Quantity")
    OTItem = models.ForeignKey('OTItem', help_text='reference to OTItem')

    objects = models.Manager()

    def __unicode__(self):
        date = defaultfilters.date(self.create_time,"SHORT_DATETIME_FORMAT")
        return u'Date:{} ____ Quantity:{} ____ Item:{}'.format(date,self.amount,self.OTItem)



class OTDIStandard(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=255, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "DI标准"

    def __unicode__(self):
        return u'{}'.format(self.name)

class OTItem(models.Model):
    '''
    Generic entity table for item
    '''
    id = models.AutoField(primary_key=True)
    part_no = models.CharField(max_length=100,unique=True)
    size = models.CharField(max_length=100,null=True)
    di_standard = models.ForeignKey('OTDIStandard')
    consignment_amount = models.PositiveIntegerField(default=0,verbose_name="consignment Quantity")
    desc = models.CharField(max_length=255, null=True, blank=True, help_text='Description of the item')

    #use for store the old value of consignment
    old_consignment_amount = None

    objects = models.Manager()

    class Meta:
        verbose_name = "货物列表"

    def __unicode__(self):
        return u'Id: %-8s ____ Part No: %-8s ____ Size: %-8s ____ Di Standard: %-8s' % (self.id, self.part_no, self.size, self.di_standard)
    def __init__(self, *args, **kwargs):
        super(OTItem, self).__init__(*args,**kwargs)
        self.old_consignment_amount = self.consignment_amount

    def save(self,*args, **kwargs):

        #if consignment_amount is detected changed, a new row will be inserted into the Consignment table
        super(OTItem, self).save(*args, **kwargs)
        if self.old_consignment_amount != self.consignment_amount:
            consignment = Consignment(amount=self.consignment_amount,OTItem=self)
            consignment.save()
        self.old_consignment_amount = self.consignment_amount



class OTItemDaily(models.Model):
    type_usage = 'U'
    type_return = 'R'
    type_delivery = 'D'

    TYPE = (
        (type_usage, '使用'),
        (type_return, '退货'),
        (type_delivery,'发货')
    )
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(auto_now_add=True)
    date = models.DateField(help_text='记录日期')
    OTItem = models.ForeignKey('OTItem')
    amount = models.PositiveIntegerField(default=0,help_text='数量需为正',verbose_name="Quantity")
    lot_no = models.CharField(max_length=100,null=True,default='0')
    type = models.CharField(max_length=1,choices=TYPE)
    old_amount = 0
    objects = models.Manager()

    class Meta:
        unique_together = ("date", "OTItem","type")
        verbose_name = '退货、发货、使用-日总表'
    def __init__(self, *args, **kwargs):
        super(OTItemDaily, self).__init__(*args,**kwargs)
        self.old_amount = self.amount
        print u'init: {}'.format(self.old_amount)
    def __unicode__(self):
        return u'Date: {} ____ Item: {} ____ Quantity: {} ____ Type: {} ____ Lot No: {}'.format(self.date, self.OTItem, self.amount, self.type, self.lot_no)

    def save(self,*args, **kwargs):
        super(OTItemDaily, self).save(*args, **kwargs)
        print u'save: new{} old{}'.format(self.amount,self.old_amount)
        difference = self.amount - self.old_amount
        if difference != 0:
          first_day_of_month = date(self.date.year,self.date.month,1)
          val = None
          try:
             val = OTItemMonthly.objects.get(date=first_day_of_month,type=self.type,OTItem=self.OTItem)
             print val
          except:
             pass
          if val is not None:
            val.amount = val.amount + difference
          else:
            val = OTItemMonthly(date=first_day_of_month,type=self.type,OTItem=self.OTItem,amount=self.amount)
          val.save()

@receiver(pre_delete,sender=OTItemDaily)
def subtract_from_monthly(sender,**kwargs):
    obj = kwargs['instance']
    val = None
    first_day_of_month = date(obj.date.year,obj.date.month,1)
    try:
        val = OTItemMonthly.objects.get(date=first_day_of_month,type=obj.type,OTItem=obj.OTItem)
        print val
    except:
        pass
    if val is not None:
        amount = val.amount - obj.amount;
        if amount < 0:
            amount = 0
        val.amount = amount;
        val.save()


class OTItemMonthly(models.Model):
    type_usage = 'U'
    type_return = 'R'
    type_delivery = 'D'

    TYPE = (
        (type_usage, '使用'),
        (type_return, '退货'),
        (type_delivery,'发货')
    )
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(auto_now_add=True)
    date = models.DateField(help_text='只能为每月的第一天')
    OTItem = models.ForeignKey('OTItem')
    amount = models.PositiveIntegerField(default=0,help_text='数量需为正',verbose_name="Quantity")
    type = models.CharField(max_length=1,choices=TYPE)
    objects = models.Manager()

    class Meta:
        unique_together = ("date", "OTItem","type")
        verbose_name = '退货、发货、使用-月总表'

    def __unicode__(self):
        return u'Month: {} ____ Item: {} ____ Quantity: {} ____ Type: {}'.format(self.date, self.OTItem, self.amount, self.type)



