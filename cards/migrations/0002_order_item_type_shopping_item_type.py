# Generated by Django 5.1 on 2024-09-10 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='item_type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='shopping',
            name='item_type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
