# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OTDIStandard'
        db.create_table(u'website_otdistandard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'website', ['OTDIStandard'])

        # Adding model 'OTItem'
        db.create_table(u'website_otitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('part_no', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('item_no', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('di_standard', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.OTDIStandard'])),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'website', ['OTItem'])

        # Adding model 'OTItemStorage'
        db.create_table(u'website_otitemstorage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.OTItem'])),
            ('total_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'website', ['OTItemStorage'])

        # Adding model 'OTItemDelivery'
        db.create_table(u'website_otitemdelivery', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('OTItem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.OTItem'])),
            ('amount', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'website', ['OTItemDelivery'])

        # Adding model 'OTItemReturn'
        db.create_table(u'website_otitemreturn', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('OTItem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.OTItem'])),
            ('amount', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'website', ['OTItemReturn'])

        # Adding model 'OTItemUsage'
        db.create_table(u'website_otitemusage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('OTItem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.OTItem'])),
            ('amount', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'website', ['OTItemUsage'])

        # Adding model 'OTItemDaily'
        db.create_table(u'website_otitemdaily', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('OTItem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.OTItem'])),
            ('amount', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'website', ['OTItemDaily'])


    def backwards(self, orm):
        # Deleting model 'OTDIStandard'
        db.delete_table(u'website_otdistandard')

        # Deleting model 'OTItem'
        db.delete_table(u'website_otitem')

        # Deleting model 'OTItemStorage'
        db.delete_table(u'website_otitemstorage')

        # Deleting model 'OTItemDelivery'
        db.delete_table(u'website_otitemdelivery')

        # Deleting model 'OTItemReturn'
        db.delete_table(u'website_otitemreturn')

        # Deleting model 'OTItemUsage'
        db.delete_table(u'website_otitemusage')

        # Deleting model 'OTItemDaily'
        db.delete_table(u'website_otitemdaily')


    models = {
        u'website.otdistandard': {
            'Meta': {'object_name': 'OTDIStandard'},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'website.otitem': {
            'Meta': {'object_name': 'OTItem'},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'di_standard': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.OTDIStandard']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_no': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'part_no': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'website.otitemdaily': {
            'Meta': {'object_name': 'OTItemDaily'},
            'OTItem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.OTItem']"}),
            'amount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'website.otitemdelivery': {
            'Meta': {'object_name': 'OTItemDelivery'},
            'OTItem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.OTItem']"}),
            'amount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'website.otitemreturn': {
            'Meta': {'object_name': 'OTItemReturn'},
            'OTItem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.OTItem']"}),
            'amount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'website.otitemstorage': {
            'Meta': {'object_name': 'OTItemStorage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.OTItem']"}),
            'total_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'website.otitemusage': {
            'Meta': {'object_name': 'OTItemUsage'},
            'OTItem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.OTItem']"}),
            'amount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['website']