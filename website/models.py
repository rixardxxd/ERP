# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm
from django.core.exceptions import ValidationError

class OTDIStandard(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=255, null=True, blank=True)

    objects = models.Manager()

    def __unicode__(self):
        return u'{} {}'.format(self.id, self.name)

class OTItem(models.Model):
    '''
    Generic entity table for item
    '''
    id = models.AutoField(primary_key=True)
    part_no = models.CharField(max_length=100)
    item_no = models.CharField(max_length=100)
    di_standard = models.ForeignKey('OTDIStandard')
    desc = models.CharField(max_length=255, null=True, blank=True, help_text='Description of the item')

    objects = models.Manager()

    def __unicode__(self):
        return u'[{}] {} {} {}'.format(self.id, self.part_no, self.item_no, self.di_standard)

class OTItemStorage(models.Model):
    '''
    Track the total quantity of each item in storage
    '''
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey('OTItem', help_text='reference to OTItem')
    total_count = models.IntegerField(default=0)

    objects = models.Manager()

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
    amount = models.IntegerField(default=0,help_text='使用数量需为负，发货数量需为正，退货数量需为负')
    type = models.CharField(max_length=1,choices=TYPE)
    objects = models.Manager()

    def __unicode__(self):
        return u'{} {} item:{} amout:{} type:{}'.format(self.id, self.date, self.OTItem, self.amount, self.type)

    def save(self,*args, **kwargs):
        if ( self.type == self.type_usage or self.type == self.type_return ) and self.amount > 0 :
            #raise ValidationError('使用数量需为负，退货数量需为负');
            return
        elif self.type == self.type_delivery and self.amount < 0:
            #raise ValidationError('发货数量需为正')
            return
        else:
            super(OTItemDaily, self).save(*args, **kwargs)




