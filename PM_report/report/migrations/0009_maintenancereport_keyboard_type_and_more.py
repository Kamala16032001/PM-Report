# Generated by Django 5.1.6 on 2025-02-12 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0008_maintenancereport_indic_tool'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenancereport',
            name='keyboard_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='maintenancereport',
            name='mouse_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
