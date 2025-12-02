from django.db import models


class Route(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)

    class Meta:
        unique_together = ('origin', 'destination')
        verbose_name = "Route"
        verbose_name_plural = "Routes"

    def __str__(self):
        return f"{self.origin} → {self.destination}"


class Flight(models.Model):
    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, related_name="flights"
    )
    airline = models.CharField(max_length=100)
    plane_type = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    price = models.PositiveIntegerField(default=0)
    seats_total = models.PositiveIntegerField(default=0)
    seats_available = models.PositiveIntegerField(default=0)
    cancel_penalty_percent = models.PositiveIntegerField(default=10)

    class Meta:
        ordering = ["date", "time"]

    def __str__(self):
        return f"{self.route} - {self.date} {self.time}"

    @property
    def is_available(self):
        return self.seats_available > 0