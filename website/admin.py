from django.contrib import admin
from models import OTItem, OTItemUsage, OTItemReturn, OTItemDelivery, OTItemStorage, OTDIStandard, OTItemDaily, Consignment

admin.site.register(OTItem)
admin.site.register(OTDIStandard)
admin.site.register(OTItemUsage)
admin.site.register(OTItemReturn)
admin.site.register(OTItemDelivery)
admin.site.register(OTItemStorage)
admin.site.register(OTItemDaily)
admin.site.register(Consignment)

class ConsignmentAdmin(admin.ModelAdmin):
    readonly_fields = ('create_time',)

