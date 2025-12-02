from django.db import models
from django.conf import settings
from flights.models import Flight


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

    price_paid = models.PositiveIntegerField()
    penalty_amount = models.PositiveIntegerField(default=0)
    final_refund = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    canceled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.flight} - {self.status}"