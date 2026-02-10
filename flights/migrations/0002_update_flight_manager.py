"""
Migration for updating FlightManager and Flight model with comprehensive manager methods.
"""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0001_initial'),
    ]

    operations = [
        # The manager change doesn't require schema changes as managers don't affect database structure
        migrations.AlterModelOptions(
            name='flight',
            options={'ordering': ['departure_time'], 'verbose_name': 'Flight', 'verbose_name_plural': 'Flights'},
        ),
    ]
