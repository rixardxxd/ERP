# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'OTItemDelivery'
        db.delete_table(u'website_otitemdelivery')

        # Deleting model 'OTItemReturn'
        db.delete_table(u'website_otitemreturn')

        # Deleting model 'OTItemUsage'
        db.delete_table(u'website_otitemusage')

        # Adding unique constraint on 'OTItem', fields ['item_no']
        db.create_unique(u'website_otitem', ['item_no'])

        # Adding unique constraint on 'OTItem', fields ['part_no']
        db.create_unique(u'website_otitem', ['part_no'])


    def backwards(self, orm):
        # Removing unique constraint on 'OTItem', fields ['part_no']
        db.delete_unique(u'website_otitem', ['part_no'])

        # Removing unique constraint on 'OTItem', fields ['item_no']
        db.delete_unique(u'website_otitem', ['item_no'])

        # Adding model 'OTItemDelivery'
        db.create_table(u'website_otitemdelivery', (
            ('amount', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('OTItem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.OTItem'])),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'website', ['OTItemDelivery'])

        # Adding model 'OTItemReturn'
        db.create_table(u'website_otitemreturn', (
            ('amount', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('OTItem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.OTItem'])),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'website', ['OTItemReturn'])

        # Adding model 'OTItemUsage'
        db.create_table(u'website_otitemusage', (
            ('amount', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('OTItem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.OTItem'])),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'website', ['OTItemUsage'])


    models = {
        u'website.consignment': {
            'Meta': {'object_name': 'Consignment'},
            'OTItem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.OTItem']"}),
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'website.otdistandard': {
            'Meta': {'object_name': 'OTDIStandard'},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'website.otitem': {
            'Meta': {'unique_together': "(('part_no', 'item_no', 'size', 'di_standard'),)", 'object_name': 'OTItem'},
            'consignment_amount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'di_standard': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.OTDIStandard']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_no': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'part_no': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        u'website.otitemdaily': {
            'Meta': {'unique_together': "(('date', 'OTItem', 'type'),)", 'object_name': 'OTItemDaily'},
            'OTItem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.OTItem']"}),
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'website.otitemmonthly': {
            'Meta': {'unique_together': "(('date', 'OTItem', 'type'),)", 'object_name': 'OTItemMonthly'},
            'OTItem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.OTItem']"}),
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'website.otitemstorage': {
            'Meta': {'object_name': 'OTItemStorage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.OTItem']"}),
            'total_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['website']