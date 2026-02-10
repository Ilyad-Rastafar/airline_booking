from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    Admin interface for Transaction model.
    
    Features:
    - Financial transaction tracking
    - Filtering by transaction type and date
    - Display of transaction amounts and descriptions
    - Custom manager usage for efficient querying
    """
    list_display = ('id', 'user', 'type', 'amount', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('user__username', 'description')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Transaction Details', {
            'fields': ('user', 'type', 'amount', 'created_at')
        }),
        ('Additional Information', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Override to use custom manager efficiently."""
        qs = super().get_queryset(request)
        return qs.select_related('user')
