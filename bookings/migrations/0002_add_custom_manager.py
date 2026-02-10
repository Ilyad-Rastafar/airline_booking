"""
Migration for adding BookingManager to Booking model with custom manager methods.
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        # The manager change doesn't require schema changes as managers don't affect database structure
        migrations.AlterModelOptions(
            name='booking',
            options={'ordering': ['-created_at'], 'verbose_name': 'Booking', 'verbose_name_plural': 'Bookings'},
        ),
    ]
