# -*- coding: utf-8 -*-
# coding=gbk
from django.db import models
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.template import defaultfilters

class Consignment(models.Model):

    class Meta:
        verbose_name = "寄卖数量表"


    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveIntegerField(default=0)
    OTItem = models.ForeignKey('OTItem', help_text='reference to OTItem')

    objects = models.Manager()

    def __unicode__(self):
        date = defaultfilters.date(self.create_time,"SHORT_DATETIME_FORMAT")
        return u'date:{} amount:{} OTItem:{}'.format(date,self.amount,self.OTItem)



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
    part_no = models.CharField(max_length=100)
    item_no = models.CharField(max_length=100)
    size = models.CharField(max_length=100,null=True)
    di_standard = models.ForeignKey('OTDIStandard')
    consignment_amount = models.PositiveIntegerField(default=0)
    desc = models.CharField(max_length=255, null=True, blank=True, help_text='Description of the item')

    #use for store the old value of consignment
    old_consignment_amount = None

    objects = models.Manager()

    class Meta:
        unique_together = ("part_no", "item_no","size","di_standard")
        verbose_name = "货物列表"

    def __unicode__(self):
        return u'part_no: {} item_no: {} size: {} di_standard: {}'.format(self.part_no, self.item_no, self.size, self.di_standard)
    def __init__(self, *args, **kwargs):
        super(OTItem, self).__init__(*args,**kwargs)
        self.old_consignment_amount = self.consignment_amount

    def save(self,*args, **kwargs):

        super(OTItem, self).save(*args, **kwargs)
        if self.old_consignment_amount != self.consignment_amount:
            consignment = Consignment(amount=self.consignment_amount,OTItem=self)
            consignment.save()
        self.old_consignment_amount = self.consignment_amount


class OTItemStorage(models.Model):
    '''
    Track the total quantity of each item in storage
    '''
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey('OTItem', help_text='reference to OTItem')
    total_count = models.IntegerField(default=0)

    objects = models.Manager()

    class Meta:
        verbose_name = "库存列表"
    def __unicode__(self):
        return u'{} {}'.format(self.item, self.total_count)

class OTItemDelivery(models.Model):
    '''
    Track the delivery history of item
    '''
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(auto_now_add=True)
    date = models.DateField(help_text='Track the date for easy query later')
    OTItem = models.ForeignKey('OTItem')
    amount = models.IntegerField(default=0)

    objects = models.Manager()

    class Meta:
        verbose_name = "发货列表"

    def __unicode__(self):
        return u'{} {} item:{} amout:{}'.format(self.id, self.date, self.OTItem, self.amount)

class OTItemReturn(models.Model):
    '''
    Track the return history of item
    '''
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(auto_now_add=True)
    date = models.DateField(help_text='Track the date for easy query later')
    OTItem = models.ForeignKey('OTItem')
    amount = models.IntegerField(default=0)

    objects = models.Manager()

    class Meta:
        verbose_name = "退货列表"
    def __unicode__(self):
        return u'{} {} item:{} amout:{}'.format(self.id, self.date, self.OTItem, self.amount)


class OTItemUsage(models.Model):
    '''
    Track the return history of item
    '''
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(auto_now_add=True)
    date = models.DateField(help_text='Track the date for easy query later')
    OTItem = models.ForeignKey('OTItem')
    amount = models.IntegerField(default=0)

    objects = models.Manager()

    class Meta:
        verbose_name = "使用列表"
    def __unicode__(self):
        return u'{} {} item:{} amout:{}'.format(self.id, self.date, self.OTItem, self.amount)



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
    amount = models.PositiveIntegerField(default=0,help_text='数量需为正')
    type = models.CharField(max_length=1,choices=TYPE)
    objects = models.Manager()

    class Meta:
        unique_together = ("date", "OTItem","type")
        verbose_name = '退货、发货、使用总表'

    def __unicode__(self):
        return u'date: {} item: {} amout: {} type: {}'.format(self.date, self.OTItem, self.amount, self.type)

    def save(self,*args, **kwargs):
        super(OTItemDaily, self).save(*args, **kwargs)


