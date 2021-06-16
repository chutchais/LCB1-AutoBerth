from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Container,DischargePort
# Register your models here.
class ContainerAdmin(admin.ModelAdmin):
    search_fields = ['container']
    list_filter = ['iso_code','load_port','dis_port','deliverly_port']
    list_display = ('__str__','ready_to_load','uploaded','iso_code','load_port','dis_port','deliverly_port')
    # list_editable = ('color','move_performa')
    fieldsets = [
        ('Basic Information',{'fields': ['bayplanfile','container','slug','ready_to_load',
        	'uploaded','upload_date','iso_code','load_port','dis_port','deliverly_port',
        	'stowage','original_stowage']}),
        ]


admin.site.register(Container,ContainerAdmin)



class DischargePortAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = []
    list_display = ('__str__','color')
    list_editable = ['color']
    # list_editable = ('color','move_performa')
    fieldsets = [
        ('Basic Information',{'fields': ['name','color']}),
        ]


admin.site.register(DischargePort,DischargePortAdmin)