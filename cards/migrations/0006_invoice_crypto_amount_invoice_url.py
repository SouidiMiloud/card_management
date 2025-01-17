# Generated by Django 5.1 on 2024-09-15 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0005_invoice_delete_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='crypto_amount',
            field=models.DecimalField(decimal_places=15, default=0.0, max_digits=20),
        ),
        migrations.AddField(
            model_name='invoice',
            name='url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
