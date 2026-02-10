from django.db import models
from django.conf import settings
from flights.models import Flight


class BookingManager(models.Manager):
    """
    Custom manager for Booking model.
    
    Provides convenient querysets for common booking-related operations:
    - active(): Filter only active (not canceled) bookings
    - canceled(): Filter only canceled bookings
    - for_user(user): Get all bookings for a specific user
    
    Why this manager exists:
    - Encapsulates booking filtering logic
    - Makes queries more readable and maintainable
    - Reduces code duplication across the application
    - Provides semantic methods that express intent
    """

    def active(self):
        """Return only active (non-canceled) bookings."""
        return self.filter(status='active')

    def canceled(self):
        """Return only canceled bookings."""
        return self.filter(status='canceled')

    def for_user(self, user):
        """Return all bookings for a specific user."""
        return self.filter(user=user)


class Booking(models.Model):

    STATUS_CHOICES = [
        ("active", "Active"),
        ("canceled", "Canceled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings"
    )
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name="bookings"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    price_paid = models.PositiveIntegerField(default=0)
    penalty_amount = models.PositiveIntegerField(default=0)
    final_refund = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    canceled_at = models.DateTimeField(null=True, blank=True)

    # Use custom manager
    objects = BookingManager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    def __str__(self):
        return f"{self.user} - {self.flight} - {self.status}"