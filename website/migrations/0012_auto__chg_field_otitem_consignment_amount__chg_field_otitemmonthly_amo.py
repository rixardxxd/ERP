# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'OTItem.consignment_amount'
        db.alter_column(u'website_otitem', 'consignment_amount', self.gf('django.db.models.fields.BigIntegerField')())

        # Changing field 'OTItemMonthly.amount'
        db.alter_column(u'website_otitemmonthly', 'amount', self.gf('django.db.models.fields.BigIntegerField')())

        # Changing field 'OTItemDaily.amount'
        db.alter_column(u'website_otitemdaily', 'amount', self.gf('django.db.models.fields.BigIntegerField')())

        # Changing field 'Consignment.amount'
        db.alter_column(u'website_consignment', 'amount', self.gf('django.db.models.fields.BigIntegerField')())

    def backwards(self, orm):

        # Changing field 'OTItem.consignment_amount'
        db.alter_column(u'website_otitem', 'consignment_amount', self.gf('django.db.models.fields.PositiveIntegerField')())

        # Changing field 'OTItemMonthly.amount'
        db.alter_column(u'website_otitemmonthly', 'amount', self.gf('django.db.models.fields.PositiveIntegerField')())

        # Changing field 'OTItemDaily.amount'
        db.alter_column(u'website_otitemdaily', 'amount', self.gf('django.db.models.fields.PositiveIntegerField')())

        # Changing field 'Consignment.amount'
        db.alter_column(u'website_consignment', 'amount', self.gf('django.db.models.fields.PositiveIntegerField')())

    models = {
        u'website.consignment': {
            'Meta': {'object_name': 'Consignment'},
            'OTItem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.OTItem']"}),
            'amount': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
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
            'Meta': {'ordering': "['item_no']", 'object_name': 'OTItem'},
            'consignment_amount': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'di_standard': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.OTDIStandard']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True', 'null': 'True'}),
            'part_no': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        u'website.otitemdaily': {
            'Meta': {'unique_together': "(('date', 'OTItem', 'type'),)", 'object_name': 'OTItemDaily'},
            'OTItem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.OTItem']"}),
            'amount': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lot_no': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '100', 'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'website.otitemmonthly': {
            'Meta': {'unique_together': "(('date', 'OTItem', 'type'),)", 'object_name': 'OTItemMonthly'},
            'OTItem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.OTItem']"}),
            'amount': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        }
    }

    complete_apps = ['website']