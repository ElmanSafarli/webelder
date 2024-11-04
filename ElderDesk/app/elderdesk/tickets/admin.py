from django.contrib import admin
from .models import Ticket, DynamicField

class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'title', 'initiator', 'assignee', 'status', 'created_date', 'updated_date')
    list_filter = ('status', 'created_date', 'updated_date')
    search_fields = ('ticket_id', 'title', 'initiator', 'assignee__name')
    filter_horizontal = ('subscribers',)  # To handle ManyToManyField
    readonly_fields = ('ticket_id', 'created_date', 'updated_date')
    ordering = ('-created_date',)

class DynamicFieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'values')
    search_fields = ('name', 'values')

admin.site.register(Ticket, TicketAdmin)
admin.site.register(DynamicField, DynamicFieldAdmin)
