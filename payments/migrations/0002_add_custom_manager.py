"""
Migration for adding TransactionManager to Transaction model with custom manager methods.
"""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        # The manager change doesn't require schema changes as managers don't affect database structure
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-created_at'], 'verbose_name': 'Transaction', 'verbose_name_plural': 'Transactions'},
        ),
    ]
