from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Admin interface for Booking model.
    
    Features:
    - List display with key booking information
    - Filtering by status and creation date
    - Search by user and flight information
    - Custom manager usage for efficient querying
    """
    list_display = ('id', 'user', 'flight', 'status', 'price_paid', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'flight__origin', 'flight__destination')
    readonly_fields = ('created_at', 'canceled_at')
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('user', 'flight', 'status', 'created_at', 'canceled_at')
        }),
        ('Financial Information', {
            'fields': ('price_paid', 'penalty_amount', 'final_refund')
        }),
    )

    def get_queryset(self, request):
        """Override to use custom manager efficiently."""
        qs = super().get_queryset(request)
        return qs.select_related('user', 'flight')