from django.db import models
from django.conf import settings


class Transaction(models.Model):
    TYPE_CHOICES = [
        ("deposit", "Deposit"),
        ("payment", "Payment"),
        ("refund", "Refund"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions"
    )
    amount = models.IntegerField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.type} - {self.amount}"