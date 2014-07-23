# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'OTItem.consignment_amount'
        db.add_column(u'website_otitem', 'consignment_amount',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'OTItem.consignment_amount'
        db.delete_column(u'website_otitem', 'consignment_amount')


    models = {
        u'website.consignment': {
            'Meta': {'unique_together': "(('date', 'OTItem'),)", 'object_name': 'Consignment'},
            'OTItem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.OTItem']"}),
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
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
            'item_no': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'part_no': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        u'website.otitemdaily': {
            'Meta': {'unique_together': "(('date', 'OTItem', 'type'),)", 'object_name': 'OTItemDaily'},
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