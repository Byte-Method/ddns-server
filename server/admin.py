from django.contrib import admin
from server.models import Client, Record


class RecordInline(admin.TabularInline):
    model = Record

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request):
        return False

    def has_delete_permission(self, request):
        return False


class RecordAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated_on'
    actions = None
    list_display_links = None
    list_display = ('update_ip', 'remote_ip', 'client__name', 'client__uuid', 'updated_on')
    list_filter = ('client__name', 'protocol')

    def has_add_permission(self, request):
        return False


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'uuid', 'domain', 'latest_record', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active',)
    inlines = [
        RecordInline,
    ]


admin.site.register(Client, ClientAdmin)
admin.site.register(Record, RecordAdmin)