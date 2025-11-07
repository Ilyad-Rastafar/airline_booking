from django.db import models


class Route(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.origin} → {self.destination}"


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    airline = models.CharField(max_length=100)
    airplane_type = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seats = models.PositiveIntegerField()
    cancellation_fee_percent = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.airline} - {self.route} ({self.date} {self.time})"
