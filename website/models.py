# -*- coding: utf-8 -*-
# coding=gbk
from django.db import models
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.template import defaultfilters
from datetime import date,datetime
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)


class Consignment(models.Model):
    class Meta:
        verbose_name = "寄卖数量表"


    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(auto_now_add=True)
    amount = models.BigIntegerField(default=0, verbose_name="Quantity")
    OTItem = models.ForeignKey('OTItem', help_text='reference to OTItem')

    objects = models.Manager()

    def __unicode__(self):
        date = defaultfilters.date(self.create_time, "SHORT_DATETIME_FORMAT")
        return u'Date:{} ____ Quantity:{} ____ Item:{}'.format(date, self.amount, self.OTItem)


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
    item_no = models.CharField(max_length=100, unique=True, null=True)
    part_no = models.CharField(max_length=100, unique=True)
    size = models.CharField(max_length=100, null=True)
    di_standard = models.ForeignKey('OTDIStandard')
    consignment_amount = models.BigIntegerField(default=0, verbose_name="consignment Quantity")
    desc = models.CharField(max_length=255, null=True, blank=True, help_text='Description of the item')

    # use for store the old value of consignment
    old_consignment_amount = None

    objects = models.Manager()

    class Meta:
        verbose_name = "货物列表"
        ordering = ['item_no']

    def __unicode__(self):
        return u'Item_No: %-8s ____ Part No: %-8s ____ Size: %-8s ____ Di Standard: %-8s' % (
            self.item_no, self.part_no, self.size, self.di_standard)

    def __init__(self, *args, **kwargs):
        super(OTItem, self).__init__(*args, **kwargs)
        self.old_consignment_amount = self.consignment_amount

    def save(self, *args, **kwargs):
        # if consignment_amount is detected changed, a new row will be inserted into the Consignment table
        super(OTItem, self).save(*args, **kwargs)
        if self.old_consignment_amount != self.consignment_amount:
            consignment = Consignment(amount=self.consignment_amount, OTItem=self)
            consignment.save()
        self.old_consignment_amount = self.consignment_amount


class OTItemDaily(models.Model):
    type_usage = 'U'
    type_return = 'R'
    type_delivery = 'D'

    TYPE = (
        (type_usage, '使用'),
        (type_return, '退货'),
        (type_delivery, '发货')
    )
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(auto_now_add=True)
    date = models.DateField(help_text='记录日期')
    OTItem = models.ForeignKey('OTItem')
    amount = models.BigIntegerField(default=0, help_text='数量需为正', verbose_name="Quantity")
    lot_no = models.CharField(max_length=100, null=True, default='0')
    type = models.CharField(max_length=1, choices=TYPE)
    objects = models.Manager()

    class Meta:
        unique_together = ("date", "OTItem", "type")
        verbose_name = '退货、发货、使用-日总表'

    def __unicode__(self):
        return u'Date: {} ____ Item: {} ____ Quantity: {} ____ Type: {} ____ Lot No: {}'.format(self.date, self.OTItem,
                                                                                                self.amount, self.type,
                                                                                                self.lot_no)


@receiver(pre_save, sender=OTItemDaily)
def add_to_monthly(sender, **kwargs):
    instance = kwargs['instance']
    logger.debug("instance id is %s, amount is %s, date is %s" % (instance.id, instance.amount, instance.date))
    # update
    if instance.id:
        old_item = OTItemDaily.objects.get(pk=instance.id)
        logger.debug("old_item %s" % str(old_item))
        first_day_of_month = date(instance.date.year, instance.date.month, 1)
        difference = 0
        if old_item:
            difference = instance.amount - old_item.amount
        else:
            difference += instance.amount
            logger.debug("difference value is %d" % difference)

        if difference != 0:
            val = None
            try:
                val = OTItemMonthly.objects.get(date=first_day_of_month, type=instance.type, OTItem=instance.OTItem)
                print val
            except Exception as e:
                logger.exception('%s' % e.message)
            if val is not None:
                val.amount = val.amount + difference
            else:
                val = OTItemMonthly(date=first_day_of_month, type=instance.type, OTItem=instance.OTItem,
                                    amount=difference)
            val.save()
    # create
    else:
        tmp = datetime.strptime(instance.date,'%Y-%m-%d')
        first_day_of_month = date(tmp.year, tmp.month, 1)
        difference = 0
        difference += instance.amount
        logger.debug("difference value is %d" % difference)

        if difference != 0:
            val = None
            try:
                val = OTItemMonthly.objects.get(date=first_day_of_month, type=instance.type, OTItem=instance.OTItem)
                print val
            except Exception as e:
                logger.exception('%s' % e.message)
            if val is not None:
                val.amount = val.amount + difference
            else:
                val = OTItemMonthly(date=first_day_of_month, type=instance.type, OTItem=instance.OTItem,
                                    amount=difference)
            val.save()


@receiver(pre_delete, sender=OTItemDaily)
def subtract_from_monthly(sender, **kwargs):
    obj = kwargs['instance']
    val = None
    first_day_of_month = date(obj.date.year, obj.date.month, 1)
    try:
        val = OTItemMonthly.objects.get(date=first_day_of_month, type=obj.type, OTItem=obj.OTItem)
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
        (type_delivery, '发货')
    )
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(auto_now_add=True)
    date = models.DateField(help_text='只能为每月的第一天')
    OTItem = models.ForeignKey('OTItem')
    amount = models.BigIntegerField(default=0, help_text='数量需为正', verbose_name="Quantity")
    type = models.CharField(max_length=1, choices=TYPE)
    objects = models.Manager()

    class Meta:
        unique_together = ("date", "OTItem", "type")
        verbose_name = '退货、发货、使用-月总表'

    def __unicode__(self):
        return u'Month: {} ____ Item: {} ____ Quantity: {} ____ Type: {}'.format(self.date, self.OTItem, self.amount,
                                                                                 self.type)



