__author__ = 'xxd'
from rest_framework import serializers
from models import OTItemDaily

class OTItemDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = OTItemDaily
        depth = 1