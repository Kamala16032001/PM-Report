# Generated by Django 5.1.6 on 2025-02-12 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0005_rename_keyboard_serial_no_maintenancereport_adobe_reader_version_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenancereport',
            name='dsc_driver_version',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='maintenancereport',
            name='laps_version',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='maintenancereport',
            name='ms_office_veraion',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='maintenancereport',
            name='os_patch',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
