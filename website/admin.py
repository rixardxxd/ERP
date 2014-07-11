from django.contrib import admin
from models import OTItem, OTItemUsage, OTItemReturn, OTItemDelivery, OTItemStorage, OTDIStandard, OTItemDaily,OTItemMonthly, Consignment

admin.site.register(OTItem)
admin.site.register(OTDIStandard)
admin.site.register(OTItemUsage)
admin.site.register(OTItemReturn)
admin.site.register(OTItemDelivery)
admin.site.register(OTItemStorage)
admin.site.register(OTItemDaily)
admin.site.register(Consignment)
admin.site.register(OTItemMonthly)


class ConsignmentAdmin(admin.ModelAdmin):
    readonly_fields = ('create_time',)
