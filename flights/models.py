from django.db import models
from django.utils import timezone


class Route(models.Model):
    """
    Model representing an airline route (origin-destination pair).
    """
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)

    class Meta:
        unique_together = ('origin', 'destination')
        verbose_name = "Route"
        verbose_name_plural = "Routes"

    def __str__(self):
        return f"{self.origin} → {self.destination}"


class FlightManager(models.Manager):
    """
    Custom manager for Flight model.
    
    Provides convenient querysets for common flight operations:
    - available(): Filter flights with available seats and future departure times
    - past(): Filter flights that have already departed
    - search(origin, destination, date): Search flights by route and date
    
    Why this manager exists:
    - Encapsulates flight availability logic
    - Centralizes search functionality
    - Makes queries more readable and semantic
    - Prevents repeated filtering logic throughout the codebase
    - Improves code maintainability and reduces bugs
    """

    def available(self):
        """Return only flights with available seats and future departure times."""
        return self.filter(
            departure_time__gte=timezone.now(),
            seats_available__gt=0
        )

    def past(self):
        """Return flights that have already departed."""
        return self.filter(departure_time__lt=timezone.now())

    def search(self, origin='', destination='', date=''):
        """
        Search flights by origin, destination, and/or date.
        
        Args:
            origin (str): Departure city (case-insensitive)
            destination (str): Arrival city (case-insensitive)
            date (str): Flight date in YYYY-MM-DD format
        
        Returns:
            QuerySet: Filtered available flights
        """
        qs = self.available()
        
        if origin:
            qs = qs.filter(origin__icontains=origin)
        if destination:
            qs = qs.filter(destination__icontains=destination)
        if date:
            qs = qs.filter(departure_time__date=date)
        
        return qs


class Flight(models.Model):
    """
    Model representing an airline flight with schedule and pricing information.
    """
    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, related_name="flights"
    )
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    price = models.PositiveIntegerField()
    seats_available = models.PositiveIntegerField()
    airplane_type = models.CharField(max_length=100)
    cancel_penalty_percent = models.PositiveIntegerField()
    airline_name = models.CharField(max_length=100)

    # Use custom manager
    objects = FlightManager()

    class Meta:
        ordering = ["departure_time"]
        verbose_name = "Flight"
        verbose_name_plural = "Flights"

    def __str__(self):
        return f"{self.origin} → {self.destination}"

    @property
    def is_available(self):
        """Check if flight has available seats."""
        return self.seats_available > 0
