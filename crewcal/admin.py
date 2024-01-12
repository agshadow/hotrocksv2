from django.contrib import admin

from .models import Job, DateEntry
from django.utils.html import format_html
from django.urls import reverse


    

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'location', 'show_dates')  # Fields to display in the list view
    search_fields = ('name', 'number', 'location')  # Fields to search for in the admin interface
    
    def show_dates(self, obj):
        dates = obj.dateentry_set.all()
        if len(dates) == 0:
            return format_html("<i>None</i>")
        
        plural=""
        if len(dates) > 1:
            plural = "s"

        parm = "?id__in=" + ",".join([str(d.id) for d in dates])
        url = reverse("admin:crewcal_dateentry_changelist") + parm
        return format_html('<a href="{}">Date_Entry{}</a>', url, plural)
    show_dates.short_description = "Dates for Job"


class JobNameFilter(admin.SimpleListFilter):
    title = 'Job Name'  # Displayed in the right sidebar
    parameter_name = 'job_name'  # URL parameter for the filter

    def lookups(self, request, model_admin):
        # Get distinct job names from the related Job model
        job_names = set(DateEntry.objects.values_list('job__name', flat=True))
        return [(name, name) for name in job_names]

    def queryset(self, request, queryset):
        # Apply the filter to the queryset based on the selected job name
        value = self.value()
        if value:
            return queryset.filter(job__name=value)
        return queryset

@admin.register(DateEntry)
class DateEntryAdmin(admin.ModelAdmin):
    list_display = ('job', 'date', 'crew', 'notes', 'quantity')
    search_fields = ('job__name', 'crew', 'notes', 'quantity')
    list_filter = (JobNameFilter,) 