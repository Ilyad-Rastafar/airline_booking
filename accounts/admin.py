from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, EmailVerificationToken


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Customized User admin with additional fields for email verification.
    """
    list_display = ('username', 'email', 'is_email_verified', 'wallet', 'is_active', 'date_joined')
    list_filter = ('is_email_verified', 'is_active', 'date_joined')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('wallet', 'is_email_verified')}),
    )
    search_fields = ('username', 'email')


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    """
    Admin interface for managing email verification tokens.
    """
    list_display = ('user', 'is_used', 'is_expired', 'created_at')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__username', 'token')
    readonly_fields = ('token', 'created_at')

    def is_expired(self, obj):
        """Display expiry status."""
        return obj.is_expired()
    is_expired.short_description = "Expired"
    is_expired.boolean = True
