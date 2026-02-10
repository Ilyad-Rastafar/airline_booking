from django.contrib import admin
from .models import Flight, Route


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    """
    Admin interface for Route model.
    """
    list_display = ('origin', 'destination')
    search_fields = ('origin', 'destination')
    ordering = ('origin', 'destination')


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    """
    Admin interface for Flight model with custom manager integration.
    
    Features:
    - Display flight schedule and pricing
    - Filter by route and availability
    - Search by origin/destination
    - Custom manager usage for efficient querying
    """
    list_display = ('id', 'route', 'departure_time', 'price', 'seats_available', 'airline_name')
    list_filter = ('airline_name', 'departure_time', 'route')
    search_fields = ('origin', 'destination', 'airline_name')
    readonly_fields = ('route',)
    
    fieldsets = (
        ('Flight Details', {
            'fields': ('route', 'origin', 'destination', 'departure_time')
        }),
        ('Capacity & Pricing', {
            'fields': ('seats_available', 'price', 'cancel_penalty_percent')
        }),
        ('Aircraft Information', {
            'fields': ('airplane_type', 'airline_name')
        }),
    )

    def get_queryset(self, request):
        """Override to use custom manager efficiently."""
        qs = super().get_queryset(request)
        return qs.select_related('route')
