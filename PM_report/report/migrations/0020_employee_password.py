# Generated by Django 5.1.6 on 2025-02-14 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0019_maintenancereport_printer_remark_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='password',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
