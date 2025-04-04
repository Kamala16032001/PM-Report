# Generated by Django 5.1.6 on 2025-02-14 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0018_alter_maintenancereport_activity_1_details_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenancereport',
            name='printer_remark',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='maintenancereport',
            name='activity_1_details',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='maintenancereport',
            name='activity_2_details',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='maintenancereport',
            name='activity_3_details',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='maintenancereport',
            name='activity_4_details',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='maintenancereport',
            name='activity_5_details',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='maintenancereport',
            name='activity_6_details',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
