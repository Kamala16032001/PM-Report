# Generated by Django 5.1.6 on 2025-02-19 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_number', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('designation', models.CharField(blank=True, max_length=100, null=True)),
                ('department', models.CharField(blank=True, max_length=100, null=True)),
                ('sro_tnso', models.CharField(blank=True, max_length=100, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pm_no', models.CharField(max_length=100)),
                ('quarter', models.CharField(max_length=50)),
                ('date', models.DateField(blank=True, null=True)),
                ('year', models.PositiveIntegerField(blank=True, null=True)),
                ('cpu_make_model', models.CharField(blank=True, max_length=255, null=True)),
                ('serial_number', models.CharField(blank=True, max_length=255, null=True)),
                ('computer_name', models.CharField(blank=True, max_length=255, null=True)),
                ('employee_number', models.CharField(blank=True, max_length=100, null=True)),
                ('employee_name', models.CharField(blank=True, max_length=100, null=True)),
                ('employee_department', models.CharField(blank=True, max_length=100, null=True)),
                ('employee_designation', models.CharField(blank=True, max_length=100, null=True)),
                ('sro_tnso', models.CharField(blank=True, max_length=100, null=True)),
                ('floor', models.CharField(blank=True, max_length=100, null=True)),
                ('location_name', models.CharField(blank=True, max_length=100, null=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('system_model', models.CharField(blank=True, max_length=255, null=True)),
                ('os_version', models.CharField(blank=True, max_length=255, null=True)),
                ('monitor_serial_number', models.CharField(blank=True, max_length=255, null=True)),
                ('mouse_serial_number', models.CharField(blank=True, max_length=255, null=True)),
                ('keyboard_serial_number', models.CharField(blank=True, max_length=255, null=True)),
                ('processor_type', models.CharField(blank=True, max_length=255, null=True)),
                ('hdd_info', models.CharField(blank=True, max_length=255, null=True)),
                ('ram_info', models.CharField(blank=True, max_length=255, null=True)),
                ('sap_version', models.CharField(blank=True, max_length=255, null=True)),
                ('java_version', models.CharField(blank=True, max_length=255, null=True)),
                ('ultravnc_version', models.CharField(blank=True, max_length=255, null=True)),
                ('adobe_reader_version', models.CharField(blank=True, max_length=255, null=True)),
                ('chrome_version', models.CharField(blank=True, max_length=255, null=True)),
                ('os_patch', models.CharField(blank=True, max_length=255, null=True)),
                ('laps_version', models.CharField(blank=True, max_length=255, null=True)),
                ('dsc_driver_version', models.CharField(blank=True, max_length=255, null=True)),
                ('ms_office_version', models.CharField(blank=True, max_length=255, null=True)),
                ('indic_tool', models.CharField(blank=True, max_length=255, null=True)),
                ('keyboard_type', models.CharField(blank=True, max_length=255, null=True)),
                ('mouse_type', models.CharField(blank=True, max_length=255, null=True)),
                ('trellix_version', models.CharField(blank=True, max_length=255, null=True)),
                ('trellix_dlp_version', models.CharField(blank=True, max_length=255, null=True)),
                ('trellix_endpoint', models.CharField(blank=True, max_length=255, null=True)),
                ('trellix_threat', models.CharField(blank=True, max_length=255, null=True)),
                ('bigfix_control', models.CharField(blank=True, max_length=255, null=True)),
                ('printer_model', models.CharField(blank=True, max_length=255, null=True)),
                ('printer_serial_number', models.CharField(blank=True, max_length=255, null=True)),
                ('printer_type', models.CharField(blank=True, max_length=255, null=True)),
                ('printer_status', models.CharField(blank=True, max_length=255, null=True)),
                ('printer_remark', models.CharField(blank=True, max_length=255, null=True)),
                ('activity_1_status', models.CharField(max_length=50, null=True)),
                ('activity_1_details', models.CharField(blank=True, max_length=500, null=True)),
                ('activity_2_status', models.CharField(max_length=50, null=True)),
                ('activity_2_details', models.CharField(blank=True, max_length=500, null=True)),
                ('activity_3_status', models.CharField(max_length=50, null=True)),
                ('activity_3_details', models.CharField(blank=True, max_length=500, null=True)),
                ('activity_4_status', models.CharField(max_length=50, null=True)),
                ('activity_4_details', models.CharField(blank=True, max_length=500, null=True)),
                ('activity_5_status', models.CharField(max_length=50, null=True)),
                ('activity_5_details', models.CharField(blank=True, max_length=500, null=True)),
                ('activity_6_status', models.CharField(max_length=50, null=True)),
                ('activity_6_details', models.CharField(blank=True, max_length=500, null=True)),
                ('pc_purpose', models.CharField(blank=True, max_length=255, null=True)),
                ('app_installed', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at_time', models.TimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
