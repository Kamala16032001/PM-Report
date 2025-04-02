from django.db import models
from django.contrib.auth.hashers import make_password

class Employee(models.Model):
    employee_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    sro_tnso = models.CharField(max_length=100, blank=True, null=True)
    location_name = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.password:  # If no password is provided, assign the default password
            self.password = make_password("Cipl@123")
        super(Employee, self).save(*args, **kwargs)
        
        
    def __str__(self):
        return f"{self.name} ({self.employee_number})"
    

class MaintenanceReport(models.Model):
    pm_no = models.CharField(max_length=100)
    quarter = models.CharField(max_length=50)
    date = models.DateField(null=True, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    cpu_make_model = models.CharField(max_length=255, null=True, blank=True)
    serial_number = models.CharField(max_length=255, null=True, blank=True)
    computer_name = models.CharField(max_length=255, null=True, blank=True)
    employee_number = models.CharField(max_length=100, null=True, blank=True)
    employee_name = models.CharField(max_length=100, null=True, blank=True)
    employee_department = models.CharField(max_length=100, null=True, blank=True)
    employee_designation = models.CharField(max_length=100, null=True, blank=True)
    sro_tnso = models.CharField(max_length=100, null=True, blank=True)
    floor = models.CharField(max_length=100, null=True, blank=True)
    location_name = models.CharField(max_length=100, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    system_model = models.CharField(max_length=255, null=True, blank=True)
    os_version = models.CharField(max_length=255, null=True, blank=True)
    monitor_serial_number = models.CharField(max_length=255, null=True, blank=True)
    mouse_serial_number = models.CharField(max_length=255, null=True, blank=True)
    keyboard_serial_number = models.CharField(max_length=255, null=True, blank=True)
    processor_type = models.CharField(max_length=255, null=True, blank=True)
    hdd_info = models.CharField(max_length=255, null=True, blank=True)
    ram_info = models.CharField(max_length=255, null=True, blank=True)
    sap_version = models.CharField(max_length=255, null=True, blank=True)
    java_version = models.CharField(max_length=255, null=True, blank=True)
    adobe_reader_version = models.CharField(max_length=255, null=True, blank=True)
    chrome_version = models.CharField(max_length=255, null=True, blank=True)
    os_patch = models.CharField(max_length=255, null=True, blank=True)
    laps_version = models.CharField(max_length=255, null=True, blank=True)
    dsc_driver_version = models.CharField(max_length=255, null=True, blank=True)
    ms_office_version = models.CharField(max_length=255, null=True, blank=True)
    indic_tool = models.CharField(max_length=255, null=True, blank=True)
    keyboard_type = models.CharField(max_length=255, null=True, blank=True)
    mouse_type = models.CharField(max_length=255, null=True, blank=True)
    trellix_version = models.CharField(max_length=255, null=True, blank=True)
    trellix_dlp_version = models.CharField(max_length=255, null=True, blank=True)
    trellix_endpoint = models.CharField(max_length=255, null=True, blank=True)
    trellix_threat = models.CharField(max_length=255, null=True, blank=True)
    bigfix_control = models.CharField(max_length=255, null=True, blank=True)
    
    printer_model = models.CharField(max_length=255, null=True, blank=True)
    printer_serial_number = models.CharField(max_length=255, null=True, blank=True)
    printer_type = models.CharField(max_length=255, null=True, blank=True)
    printer_status = models.CharField(max_length=255, null=True, blank=True)
    printer_remark = models.CharField(max_length=255, null=True, blank=True)
    
    activity_1_status = models.CharField(max_length=50, null=True)
    activity_1_details = models.CharField(max_length=500, blank=True, null=True)
    activity_2_status = models.CharField(max_length=50, null=True)
    activity_2_details = models.CharField(max_length=500, blank=True, null=True)
    activity_3_status = models.CharField(max_length=50, null=True)
    activity_3_details = models.CharField(max_length=500, blank=True, null=True)
    activity_4_status = models.CharField(max_length=50, null=True)
    activity_4_details = models.CharField(max_length=500, blank=True, null=True)
    activity_5_status = models.CharField(max_length=50, null=True)
    activity_5_details = models.CharField(max_length=500, blank=True, null=True)
    activity_6_status = models.CharField(max_length=50, null=True)
    activity_6_details = models.CharField(max_length=500, blank=True, null=True)

    pc_purpose = models.CharField(max_length=255, null=True, blank=True)
    app_installed = models.CharField(max_length=255, null=True, blank=True)
    
    created_at_time = models.TimeField(auto_now_add=True, blank=True, null=True)
    
    # class Meta:
    #     ordering = [
    #         'pm_no', 'quarter', 'year', 'date', 'created_at_time', 'employee_number', 'employee_name', 
    #         'employee_department', 'employee_designation', 'sro_tnso', 'floor', 'location_name',
    #         'ip_address','cpu_make_model', 'serial_number', 'computer_name', 'monitor_serial_number','system_model',
    #         'os_version', 'keyboard_type', 'keyboard_serial_number', 'mouse_type', 'mouse_serial_number',
    #         'processor_type', 'hdd_info', 'ram_info', 'sap_version', 'java_version',
    #         'ultravnc_version', 'adobe_reader_version', 'chrome_version', 'os_patch', 'laps_version',
    #         'dsc_driver_version', 'ms_office_version', 'indic_tool', 
    #         'trellix_version', 'trellix_dlp_version', 'trellix_endpoint', 'trellix_threat', 'bigfix_control',
    #         'printer_model', 'printer_serial_number', 'printer_type', 'printer_status', 'printer_remark',
    #         'activity_1_status', 'activity_1_details', 'activity_2_status', 'activity_2_details',
    #         'activity_3_status', 'activity_3_details', 'activity_4_status', 'activity_4_details',
    #         'activity_5_status', 'activity_5_details', 'activity_6_status', 'activity_6_details',
    #         'pc_purpose', 'app_installed'
    #     ]
    
    def __str__(self):
        return f"PM No: {self.pm_no} - {self.year} - {self.location_name}"
    
    def formatted_time(self):
        # Format time to show only hour:minute:second
        return self.created_at_time.strftime('%H:%M:%S')

