from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    
    Fields:
    - email: User email address (inherited from AbstractUser)
    - username: Unique username (inherited from AbstractUser)
    - password: Hashed password (inherited from AbstractUser)
    - is_active: Whether account is active (inherited from AbstractUser)
    - wallet: User's wallet balance for payments
    - is_email_verified: Whether user has verified their email address
    """
    wallet = models.PositiveIntegerField(default=0)
    is_email_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username


class EmailVerificationToken(models.Model):
    """
    Model to store email verification tokens for user registration.
    
    Tokens expire after 24 hours for security.
    Each token is associated with a user and contains a unique token string.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="email_verification")
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Email Verification Token"
        verbose_name_plural = "Email Verification Tokens"

    def is_expired(self):
        """Check if token has expired (24 hours)."""
        expiry_time = self.created_at + timedelta(hours=24)
        return timezone.now() > expiry_time

    def __str__(self):
        return f"Token for {self.user.username}"