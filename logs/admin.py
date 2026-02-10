from django.contrib import admin
from .models import Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    """
    Admin interface for Log model.
    
    Displays activity logs for auditing and monitoring purposes.
    Allows filtering by action type, user, and timestamp.
    """
    list_display = ('id', 'user', 'action', 'timestamp', 'ip_address')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'details', 'ip_address')
    readonly_fields = ('timestamp', 'user', 'action', 'details', 'ip_address')
    
    def has_add_permission(self, request):
        """Prevent manual addition of logs - should only be created by system."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of logs - maintain audit trail."""
        return False

    def get_queryset(self, request):
        """Override to use select_related efficiently."""
        qs = super().get_queryset(request)
        return qs.select_related('user')
