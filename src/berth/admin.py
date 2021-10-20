from django.contrib import admin

# Register your models here.
from .models import Terminal,Vessel,Service,Voy,ReportFile,cutoff

# from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter
from datetime import date
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
import copy

# from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter

from django.utils.text import slugify

def copy_new_voy(self, request, queryset):
    
    if queryset.count() >1 :
        self.message_user(request, "Not support multiple Voy selection" ,level=messages.ERROR)
        return None
    from datetime import timedelta
    for obj in queryset:
        print (obj.voy)
        new_obj = copy.copy(obj)
        # initial Data
        new_obj.id= None
        new_obj.voy = obj.voy+'_draft'
        new_obj.performa_in = obj.performa_in + timedelta(days=7)
        new_obj.performa_out = obj.performa_out + timedelta(days=7)
        new_obj.eta = obj.eta + timedelta(days=7)
        new_obj.etb = obj.etb + timedelta(days=7)
        new_obj.etd = obj.etd + timedelta(days=7)
        new_obj.imp_release_date = obj.imp_release_date + timedelta(days=7) if obj.imp_release_date != None else  obj.imp_release_date
        new_obj.export_cutoff_date = obj.export_cutoff_date + timedelta(days=7) if obj.export_cutoff_date != None else  obj.export_cutoff_date
        new_obj.draft = True
        # on June 12,2021 --added new 
        new_obj.slug = slugify(obj.voy + '-' + new_obj.code + '-' + new_obj.etb.strftime('%Y%m%d'))
        new_obj.save()

    self.message_user(request, "Draft fo %s successfully create Locker ports." % new_obj.voy)

copy_new_voy.short_description = "Copy to new Voy"

class ETAListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('ETA range')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'eta'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('today', _('Today')),
            ('thisweek', _('This week')),
            ('nextweek', _('Next week')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        from datetime import date
        if self.value() == 'today':
            today = date.today()
            return queryset.filter(eta__year=today.year,eta__month=today.month,eta__day=today.day).order_by('eta')
        if self.value() == 'thisweek':
            import datetime
            date = datetime.date.today()
            start_week = date - datetime.timedelta(date.weekday())
            end_week = start_week + datetime.timedelta(7)
            return queryset.filter(eta__range=[start_week, end_week]).order_by('eta')

        if self.value() == 'nextweek':
            import datetime
            date = datetime.date.today()
            start_week = date - datetime.timedelta(date.weekday())
            end_week = start_week + datetime.timedelta(7)
            date = end_week + datetime.timedelta(days=1)
            start_week = date - datetime.timedelta(date.weekday())
            end_week = start_week + datetime.timedelta(7)
            return queryset.filter(eta__range=[start_week, end_week]).order_by('eta')

class ETBListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('ETB range')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'etb'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('today', _('Today')),
            ('thisweek', _('This week')),
            ('nextweek', _('Next week')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        from datetime import date
        if self.value() == 'today':
            today = date.today()
            return queryset.filter(etb__year=today.year,etb__month=today.month,etb__day=today.day).order_by('etb')
        if self.value() == 'thisweek':
            import datetime
            date = datetime.date.today()
            start_week = date - datetime.timedelta(date.weekday())
            end_week = start_week + datetime.timedelta(7)
            return queryset.filter(etb__range=[start_week, end_week]).order_by('etb')

        if self.value() == 'nextweek':
            import datetime
            date = datetime.date.today()
            start_week = date - datetime.timedelta(date.weekday())
            end_week = start_week + datetime.timedelta(7)
            date = end_week + datetime.timedelta(days=1)
            start_week = date - datetime.timedelta(date.weekday())
            end_week = start_week + datetime.timedelta(7)
            return queryset.filter(etb__range=[start_week, end_week]).order_by('etb')

class ETDListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('ETD range')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'etd'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('today', _('Today')),
            ('thisweek', _('This week')),
            ('nextweek', _('Next week')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        from datetime import date
        if self.value() == 'today':
            today = date.today()
            return queryset.filter(etd__year=today.year,etd__month=today.month,etd__day=today.day).order_by('etd')
        if self.value() == 'thisweek':
            import datetime
            date = datetime.date.today()
            start_week = date - datetime.timedelta(date.weekday())
            end_week = start_week + datetime.timedelta(7)
            return queryset.filter(etd__range=[start_week, end_week]).order_by('etd')

        if self.value() == 'nextweek':
            import datetime
            date = datetime.date.today()
            start_week = date - datetime.timedelta(date.weekday())
            end_week = start_week + datetime.timedelta(7)
            date = end_week + datetime.timedelta(days=1)
            start_week = date - datetime.timedelta(date.weekday())
            end_week = start_week + datetime.timedelta(7)
            return queryset.filter(etd__range=[start_week, end_week]).order_by('etd')


# class VoyForm(forms.ModelForm):
#     class Meta:
#         model = Voy

#     def clean(self):
#         etb_date = self.cleaned_data.get('etb')
#         etd_date = self.cleaned_data.get('etd')
#         if start_date >= end_date:
#             raise forms.ValidationError("ETD date must be Bigger than ETB")
#         return self.cleaned_data

class VoyListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Voy Performing')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'perform'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('arriving', _('Berthing & Arriving')),
            ('departure', _('Departured')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        from datetime import date
        # if self.value() == 'today':
        #     today = date.today()
        #     return queryset.filter(eta__year=today.year,eta__month=today.month,eta__day=today.day).order_by('eta')
        if self.value() == 'departure':
            import datetime
            date = datetime.date.today()
            # start_week = date - datetime.timedelta(date.weekday())
            # end_week = start_week + datetime.timedelta(7)
            start_week = date - datetime.timedelta(7)
            end_week = date + datetime.timedelta(1)
            # print (start_week, end_week)
            return queryset.filter(etd__range=[start_week, end_week],
                                    vessel__v_type__in =('VESSEL','BARGE')).order_by('-etd')

        if self.value() == 'arriving':
            import datetime
            date = datetime.date.today()
            # start_week = date - datetime.timedelta(date.weekday())
            # end_week = start_week + datetime.timedelta(7)
            # date = end_week + datetime.timedelta(days=1)
            # start_week = date - datetime.timedelta(date.weekday())
            # end_week = start_week + datetime.timedelta(7)
            start_week = date - datetime.timedelta(3)
            end_week = date + datetime.timedelta(7)
            return queryset.filter(etb__range=[start_week, end_week],
                                    etd__gt = date,
                                    vessel__v_type__in =('VESSEL','BARGE')).order_by('etb')

class VoyAdmin(admin.ModelAdmin):
    search_fields = ['voy','code','vessel__name','service__name','terminal__name','vsl_oper','remark']
    list_filter = (VoyListFilter,'terminal','vessel__v_type',ETAListFilter,ETBListFilter,ETDListFilter,'draft')
    list_display = ('service','vessel','code','voy','terminal','performa_in','performa_out',
        'eta','etb','etd','dis_no','load_no','est_teu','arrival_draft','vsl_oper')
    fieldsets = [
        ('Basic Information',{'fields': [('voy'),'code',('service','vessel','vsl_oper'),
        	('terminal','start_pos','inverse'),('arrival_draft','departure_draft'),'remark']}),
        ('Performa',{'fields': [('performa_in','performa_out'),'move_confirm']}),
        ('Container Information',{'fields': [('dis_no','load_no'),'est_teu','qc']}),
        ('Estimate Time',{'fields': [('eta','etb','etd')]}),
        ('Import/Export Control',{'fields': [('export_cutoff_date')]}),
        ('Save as Draft',{'fields': [('draft'),'text_pos']}),
        # ('Bay Plan',{'fields': [('bayplanfile__filename'),'bayplanfile__uploaded']}),
    ]
    actions =[copy_new_voy]
    # save_as = True
    save_as_continue = True
    save_on_top =True
    list_select_related = True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "vessel":
            kwargs["queryset"] = Vessel.objects.order_by('name')
        return super(VoyAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Voy,VoyAdmin)




class ServiceAdmin(admin.ModelAdmin):
    search_fields = ['name','description']
    list_filter = []
    list_display = ('name','description','color','move_performa','status')
    list_editable = ('color','move_performa')
    # save_as = True
    save_as_continue = True
    save_on_top =True
    list_select_related = True
    fieldsets = [
        ('Basic Information',{'fields': ['name','description','color','move_performa','status']}),
    ]
admin.site.register(Service,ServiceAdmin)


class TerminalAdmin(admin.ModelAdmin):
    search_fields = ['name','description']
    list_filter = []
    list_display = ('name','description','start_range','stop_range','status')
    # list_editable = ('color',)
    # save_as = True
    save_as_continue = True
    save_on_top =True
    list_select_related = True
    fieldsets = [
        ('Basic Information',{'fields': ['name','description','status']}),
    ]
admin.site.register(Terminal,TerminalAdmin)



class VesselAdmin(admin.ModelAdmin):
    search_fields = ['name','imo','description']
    list_filter = ['v_type']
    list_display = ('name','description','lov','imo','v_type','status')
    # list_editable = ('color',)
    # save_as = True
    save_as_continue = True
    save_on_top =True
    list_select_related = True
    fieldsets = [
        ('Basic Information',{'fields': ['name','description','lov','imo','v_type','status']}),
    ]
admin.site.register(Vessel,VesselAdmin)




admin.site.register(ReportFile)



class CutOffAdmin(admin.ModelAdmin):
    search_fields = ['voy']
    list_filter = ['voy__service']
    list_display = ['voy','dry_date','return_date']
    # save_as = True
    save_as_continue = True
    save_on_top =True
    list_select_related = True
    raw_id_fields = ['voy']
    fieldsets = [
        ('Basic Information',{'fields': [('voy'),'dry_date','reef_date','chilled_date','durian_date','return_date' ]}),
        ]

admin.site.register(cutoff,CutOffAdmin)

