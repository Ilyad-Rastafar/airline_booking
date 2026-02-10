from django.db import models
from django.conf import settings


class TransactionManager(models.Manager):
    """
    Custom manager for Transaction model.
    
    Provides convenient querysets for financial transaction filtering:
    - deposits(): Filter only deposit transactions
    - payments(): Filter only payment transactions
    - refunds(): Filter only refund transactions
    - for_user(user): Get all transactions for a specific user
    
    Why this manager exists:
    - Centralizes transaction filtering logic
    - Simplifies financial reporting and analysis
    - Makes queries more expressive and readable
    - Prevents SQL mistakes in transaction filtering
    - Facilitates audit trails and financial records
    """

    def deposits(self):
        """Return only deposit transactions."""
        return self.filter(type='deposit')

    def payments(self):
        """Return only payment transactions."""
        return self.filter(type='payment')

    def refunds(self):
        """Return only refund transactions."""
        return self.filter(type='refund')

    def for_user(self, user):
        """Return all transactions for a specific user."""
        return self.filter(user=user)

    def recent(self, limit=10):
        """Return the most recent transactions."""
        return self.all()[:limit]


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
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="payment")
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    # Use custom manager
    objects = TransactionManager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.user} - {self.type} - {self.amount}"