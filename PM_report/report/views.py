# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import MaintenanceReport
from django.contrib.auth.decorators import login_required
from .models import Employee
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from report.utils.captcha_generator import generate_captcha_text
import random
import string
import platform
import psutil
import socket
import subprocess
import os
import winreg
import pythoncom
import wmi
import win32com.client
 
from django.contrib.auth import authenticate, login


def view_report(request):
    quarter_search = request.GET.get('quarter', None)
    if quarter_search:
        reports = MaintenanceReport.objects.filter(quarter=quarter_search)
    else:
        reports = MaintenanceReport.objects.all()
    for report in reports:
        employee = Employee.objects.filter(employee_number=report.employee_number).first()
        if employee:
            report.employee_name = employee.name
            report.employee_number = employee.employee_number
            report.employee_department = employee.department
            report.employee_designation = employee.designation
        else:
            report.employee_name = 'N/A'
            report.employee_department = 'N/A'
            report.employee_designation = 'N/A'

    context = {
        'reports': reports,
        'quarter_search': quarter_search,  # Keep the quarter in the context to retain the search value
    }
    return render(request, 'view_report.html', context)


def choice_page(request):
    return render(request, 'choice_page.html')

# Function to generate CAPTCHA text
def generate_captcha_text(length=6):
    """Generate a random alphanumeric string with uppercase letters and digits."""
    characters = string.ascii_uppercase + string.digits  # A-Z, 0-9
    captcha_text = ''.join(random.choices(characters, k=length))
    return captcha_text


def login_view(request):
    system_username = os.environ.get('USERNAME')
    
    if request.method == 'GET':
        captcha_text = generate_captcha_text()
        request.session['captcha'] = captcha_text
        return render(request, 'login.html', {'captcha_text': captcha_text, 'employee_number': system_username})

        
    if request.method == 'POST':
        employee_number = request.POST.get('employee_number')
        password_input = request.POST.get('password')
        captcha_input = request.POST.get('captcha')
        captcha_text = request.session.get('captcha')

        if captcha_text != captcha_input:
            new_captcha = generate_captcha_text()
            request.session['captcha'] = new_captcha
            messages.error(request, "Invalid CAPTCHA. Please try again.")
            return render(request, 'login.html', {
                'captcha_text': new_captcha, 
                'employee_number': system_username
                })

        try:
            employee = Employee.objects.get(employee_number=employee_number)
            if check_password(password_input, employee.password):  # Use check_password here
                return redirect('employee_details', employee_number=employee.employee_number)
            else:
                messages.error(request, "Incorrect password. Please try again.")
                return render(request, 'login.html', {
                    'captcha_text': captcha_text, 
                    'employee_number': system_username
                    })
        except Employee.DoesNotExist:
            messages.error(request, "Employee number not found!")
            return render(request, 'login.html', {
                'captcha_text': captcha_text,
                'employee_number': system_username
                })

    # If GET request or first time visit, generate and set the CAPTCHA
    captcha_text = generate_captcha_text()
    request.session['captcha'] = captcha_text
    return render(request, 'login.html', {'captcha_text': captcha_text})


def employee_details(request, employee_number):
    try:
        employee = Employee.objects.get(employee_number=employee_number)
        if request.method == 'POST':
            quarter = request.POST.get('quarter')
            return redirect('maintenance_report', employee_number=employee_number, quarter=quarter)
        context = {
            'employee': employee,
            'employee_number': employee.employee_number,
            'employee_name': employee.name,
            'employee_designation': employee.designation,
            'employee_department': employee.department,
        }
        return render(request, 'employee_details.html', context)
    except Employee.DoesNotExist:
        return HttpResponse("Employee not found.", status=404)
   

def quarter_selection(request):
    if request.method == 'POST':
        quarter = request.POST.get('quarter')
        return redirect('maintenance_report_common', quarter=quarter)
    return render(request, 'quarter_selection.html')


# @login_required
def maintenance_report(request, employee_number, quarter): 
    try:
        employee = Employee.objects.get(employee_number=employee_number)
        if request.method == 'POST':
            pm_no = request.POST.get('pm_no')
            quarter = request.POST.get('quarter')
            date = request.POST.get('date')
            year = None
            if date:
                year = datetime.strptime(date, "%Y-%m-%d").year
            else:
                year = datetime.now().year
            cpu_make_model = request.POST.get('cpu_make_model')
            serial_number = request.POST.get('serial_number')
            computer_name = request.POST.get('computer_name')
            employee_number = request.POST.get('employee_number')
            ip_address = request.POST.get('ip_address')
            system_model = request.POST.get('system_model')
            os_version = request.POST.get('os_version')
            monitor_serial_number = request.POST.get('monitor_serial_number')
            mouse_serial_number = request.POST.get('mouse_serial_number')
            keyboard_serial_number = request.POST.get('keyboard_serial_number')
            sap_version = request.POST.get('sap_version')
            chrome_version = request.POST.get('chrome_version')
            java_version = request.POST.get('java_version')
            adobe_reader_version = request.POST.get('adobe_reader_version')
            processor_type = request.POST.get('processor_type')
            ram_info = request.POST.get('ram_info')
            hdd_info = request.POST.get('hdd_info')
            os_patch = request.POST.get('os_patch')
            laps_version = request.POST.get('laps_version')
            dsc_driver_version = request.POST.get('dsc_driver_version')
            ms_office_version = request.POST.get('ms_office_version')
            indic_tool = request.POST.get('indic_tool')
            keyboard_type = request.POST.get('keyboard_type')
            mouse_type = request.POST.get('mouse_type')
            trellix_dlp_version = request.POST.get('trellix_dlp_version')
            trellix_version = request.POST.get('trellix_version')
            trellix_endpoint = request.POST.get('trellix_endpoint')
            trellix_threat = request.POST.get('trellix_threat')
            bigfix_control = request.POST.get('bigfix_control')
            pc_purpose = request.POST.get('pc_purpose')
            app_installed = request.POST.get('app_installed')
            floor = request.POST.get('floor')
            
            printer_model = request.POST.get('printer_model')
            printer_serial_number = request.POST.get('printer_serial_number')
            printer_type = request.POST.get('printer_type')
            printer_status = request.POST.get('printer_status')
            printer_remark = request.POST.get('printer_remark')
            
            activity_1_status = request.POST.get('activity_1_status')
            activity_1_details = request.POST.get('activity_1_details')
            activity_2_status = request.POST.get('activity_2_status')
            activity_2_details = request.POST.get('activity_2_details')
            activity_3_status = request.POST.get('activity_3_status')
            activity_3_details = request.POST.get('activity_3_details')
            activity_4_status = request.POST.get('activity_4_status')
            activity_4_details = request.POST.get('activity_4_details')
            activity_5_status = request.POST.get('activity_5_status')
            activity_5_details = request.POST.get('activity_5_details')
            activity_6_status = request.POST.get('activity_6_status')
            activity_6_details = request.POST.get('activity_6_details')

            
            if not pm_no:
                quarter_mapping = {'q1': 1, 'q2': 2, 'q3': 3, 'q4': 4}
                pm_no = quarter_mapping.get(quarter.lower(), None)
            if not pm_no:
                messages.error(request, "PM No is required.")
                return render(request, 'maintenance_report.html', {'employee': employee, 'quarter': quarter})

            ## Save the data to the model
            # report = MaintenanceReport(
            #     pm_no=pm_no,
            #     quarter=quarter,
            #     date=date,
            #     year=year,
            #     cpu_make_model=cpu_make_model,
            #     serial_number=serial_number,
            #     computer_name=computer_name,
            #     employee_number=employee_number,
            #     employee_name=employee.name,
            #     employee_department=employee.department,
            #     employee_designation=employee.designation,
            #     location_name=employee.location_name,
            #     sro_tnso=employee.sro_tnso,
            #     ip_address=ip_address,
            #     system_model=system_model,
            #     os_version=os_version,
            #     monitor_serial_number=monitor_serial_number,
            #     mouse_serial_number=mouse_serial_number,
            #     keyboard_serial_number=keyboard_serial_number,
            #     sap_version=sap_version,
            #     adobe_reader_version=adobe_reader_version,
            #     java_version=java_version,
            #     chrome_version=chrome_version,
            #     processor_type=processor_type,
            #     hdd_info=hdd_info,
            #     ram_info=ram_info,
            #     os_patch=os_patch,
            #     laps_version=laps_version,
            #     dsc_driver_version=dsc_driver_version,
            #     ms_office_version=ms_office_version,
            #     indic_tool=indic_tool,
            #     keyboard_type=keyboard_type,
            #     mouse_type=mouse_type,
            #     trellix_dlp_version=trellix_dlp_version,
            #     trellix_version=trellix_version,
            #     trellix_endpoint=trellix_endpoint,
            #     trellix_threat=trellix_threat,
            #     bigfix_control=bigfix_control,
            #     pc_purpose=pc_purpose,
            #     app_installed=app_installed,
            #     floor=floor,
                
            #     printer_model=printer_model,
            #     printer_serial_number=printer_serial_number,
            #     printer_type=printer_type,
            #     printer_status=printer_status,
            #     printer_remark=printer_remark,
                
            #     activity_1_status=activity_1_status,
            #     activity_1_details=activity_1_details,
            #     activity_2_status=activity_2_status,
            #     activity_2_details=activity_2_details,
            #     activity_3_status=activity_3_status,
            #     activity_3_details=activity_3_details,
            #     activity_4_status=activity_4_status,
            #     activity_4_details=activity_4_details,
            #     activity_5_status=activity_5_status,
            #     activity_5_details=activity_5_details,
            #     activity_6_status=activity_6_status,
            #     activity_6_details=activity_6_details,

            # )
            # report.save()
            # return redirect('maintenance_report_success')
            
            form_data = {
                    'pm_no': pm_no,
                    'quarter': quarter,
                    'date': date,
                    'year': year,
                    'cpu_make_model': cpu_make_model,
                    'serial_number': serial_number,
                    'computer_name': computer_name,
                    'employee_number': employee_number,
                    'employee_name': employee.name,
                    'employee_department': employee.department,
                    'employee_designation': employee.designation,
                    'location_name': employee.location_name,
                    'sro_tnso': employee.sro_tnso,
                    'ip_address': ip_address,
                    'system_model': system_model,
                    'os_version': os_version,
                    'monitor_serial_number': monitor_serial_number,
                    'mouse_serial_number': mouse_serial_number,
                    'keyboard_serial_number': keyboard_serial_number,
                    'sap_version': sap_version,
                    'adobe_reader_version': adobe_reader_version,
                    'java_version': java_version,
                    'chrome_version': chrome_version,
                    'processor_type': processor_type,
                    'hdd_info': hdd_info,
                    'ram_info': ram_info,
                    'os_patch': os_patch,
                    'laps_version': laps_version,
                    'dsc_driver_version': dsc_driver_version,
                    'ms_office_version': ms_office_version,
                    'indic_tool': indic_tool,
                    'keyboard_type': keyboard_type,
                    'mouse_type': mouse_type,
                    'trellix_dlp_version': trellix_dlp_version,
                    'trellix_version': trellix_version,
                    'trellix_endpoint': trellix_endpoint,
                    'trellix_threat': trellix_threat,
                    'bigfix_control': bigfix_control,
                    'pc_purpose': pc_purpose,
                    'app_installed': app_installed,
                    'floor': floor,
                    
                    'printer_model': printer_model,
                    'printer_serial_number': printer_serial_number,
                    'printer_type': printer_type,
                    'printer_status': printer_status,
                    'printer_remark': printer_remark,
                    
                    'activity_1_status': activity_1_status,
                    'activity_1_details': activity_1_details,
                    'activity_2_status': activity_2_status,
                    'activity_2_details': activity_2_details,
                    'activity_3_status': activity_3_status,
                    'activity_3_details': activity_3_details,
                    'activity_4_status': activity_4_status,
                    'activity_4_details': activity_4_details,
                    'activity_5_status': activity_5_status,
                    'activity_5_details': activity_5_details,
                    'activity_6_status': activity_6_status,
                    'activity_6_details': activity_6_details,

                }
        
            request.session['form_data'] = form_data
            return redirect('validate_password', employee_number=employee_number)
        
    
            # report.save()
            # return redirect('maintenance_report_success')
        
        quarter_mapping = {'q1': 1, 'q2': 2, 'q3': 3, 'q4': 4}
        pm_no = quarter_mapping.get(quarter.lower(), None)

        if pm_no is None:
            pm_no = "N/A"

        context = {
            'employee': employee,
            'employee_number': employee_number,
            'employee_name': employee.name,
            'employee_designation': employee.designation,
            'employee_department': employee.department,
            'sro_tnso': employee.sro_tnso,
            'location_name': employee.location_name,
            'quarter': quarter,
            'pm_no': pm_no,
            
        }
        return render(request, 'maintenance_report.html', context)
    except Employee.DoesNotExist:
        return HttpResponse("Employee not found.", status=404)


def validate_password(request,employee_number):
    if request.method == 'POST':
        ad_password = request.POST.get('ad_password')
        employee_number = request.POST.get('employee_number')
        
        if not employee_number:
            messages.error(request, "Employee number is required.")
            return render(request, 'validate_password.html')
        
        try:
            employee = Employee.objects.get(employee_number=employee_number)
        except Employee.DoesNotExist:
            messages.error(request, "Employee number not found.")
            return render(request, 'validate_password.html')
        
        user = authenticate(request, username=employee_number, password=ad_password)

        if user is not None:
            # Password is correct, now save the form data to the database
            form_data = request.session.get('form_data', {})
            if not form_data:
                messages.error(request, "No form data found.")
                return redirect('maintenance_report') 
            report = MaintenanceReport(
                pm_no=form_data.get('pm_no'),
                quarter=form_data.get('quarter'),
                date=form_data.get('date'),
                year=form_data.get('year'),
                cpu_make_model=form_data.get('cpu_make_model'),
                serial_number=form_data.get('serial_number'),
                computer_name=form_data.get('computer_name'),
                employee_number=form_data.get('employee_number'),
                employee_name=form_data.get('employee.name'),
                employee_department=form_data.get('employee.department'),
                employee_designation=form_data.get('employee.designation'),
                location_name=form_data.get('employee.location_name'),
                sro_tnso=form_data.get('employee.sro_tnso'),
                ip_address=form_data.get('ip_address'),
                system_model=form_data.get('system_model'),
                os_version=form_data.get('os_version'),
                monitor_serial_number=form_data.get('monitor_serial_number'),
                mouse_serial_number=form_data.get('mouse_serial_number'),
                keyboard_serial_number=form_data.get('keyboard_serial_number'),
                sap_version=form_data.get('sap_version'),
                adobe_reader_version=form_data.get('adobe_reader_version'),
                java_version=form_data.get('java_version'),
                chrome_version=form_data.get('chrome_version'),
                processor_type=form_data.get('processor_type'),
                hdd_info=form_data.get('hdd_info'),
                ram_info=form_data.get('ram_info'),
                os_patch=form_data.get('os_patch'),
                laps_version=form_data.get('laps_version'),
                dsc_driver_version=form_data.get('dsc_driver_version'),
                ms_office_version=form_data.get('ms_office_version'),
                indic_tool=form_data.get('indic_tool'),
                keyboard_type=form_data.get('keyboard_type'),
                mouse_type=form_data.get('mouse_type'),
                trellix_dlp_version=form_data.get('trellix_dlp_version'),
                trellix_version=form_data.get('trellix_version'),
                trellix_endpoint=form_data.get('trellix_endpoint'),
                trellix_threat=form_data.get('trellix_threat'),
                bigfix_control=form_data.get('bigfix_control'),
                pc_purpose=form_data.get('pc_purpose'),
                app_installed=form_data.get('app_installed'),
                floor=form_data.get('floor'),
                
                printer_model=form_data.get('printer_model'),
                printer_serial_number=form_data.get('printer_serial_number'),
                printer_type=form_data.get('printer_type'),
                printer_status=form_data.get('printer_status'),
                printer_remark=form_data.get('printer_remark'),
                
                activity_1_status=form_data.get('activity_1_status'),
                activity_1_details=form_data.get('activity_1_details'),
                activity_2_status=form_data.get('activity_2_status'),
                activity_2_details=form_data.get('activity_2_details'),
                activity_3_status=form_data.get('activity_3_status'),
                activity_3_details=form_data.get('activity_3_details'),
                activity_4_status=form_data.get('activity_4_status'),
                activity_4_details=form_data.get('activity_4_details'),
                activity_5_status=form_data.get('activity_5_status'),
                activity_5_details=form_data.get('activity_5_details'),
                activity_6_status=form_data.get('activity_6_status'),
                activity_6_details=form_data.get('activity_6_details'),

            )
            report.save()
            del request.session['form_data']
            return redirect('maintenance_report_success')
        else:
            # If the AD password is incorrect, show an error message
            messages.error(request, "Incorrect password. Please try again.")
            return render(request, 'validate_password.html', {'employee_number': employee_number})  # Re-render the password form again
    
    # If GET request, just render the password input form
    return render(request, 'validate_password.html', {'employee_number': employee_number})
        

def maintenance_report_common(request, quarter): 
    try:
        if request.method == 'POST':
            pm_no = request.POST.get('pm_no')
            quarter = request.POST.get('quarter')
            date = request.POST.get('date')
            year = None
            if date:
                year = datetime.strptime(date, "%Y-%m-%d").year
            else:
                year = datetime.now().year
            cpu_make_model = request.POST.get('cpu_make_model')
            serial_number = request.POST.get('serial_number')
            computer_name = request.POST.get('computer_name')
            ip_address = request.POST.get('ip_address')
            sro_tnso = request.POST.get('sro_tnso')
            system_model = request.POST.get('system_model')
            os_version = request.POST.get('os_version')
            monitor_serial_number = request.POST.get('monitor_serial_number')
            mouse_serial_number = request.POST.get('mouse_serial_number')
            keyboard_serial_number = request.POST.get('keyboard_serial_number')
            sap_version = request.POST.get('sap_version')
            chrome_version = request.POST.get('chrome_version')
            java_version = request.POST.get('java_version')
            adobe_reader_version = request.POST.get('adobe_reader_version')
            processor_type = request.POST.get('processor_type')
            ram_info = request.POST.get('ram_info')
            hdd_info = request.POST.get('hdd_info')
            os_patch = request.POST.get('os_patch')
            laps_version = request.POST.get('laps_version')
            dsc_driver_version = request.POST.get('dsc_driver_version')
            ms_office_version = request.POST.get('ms_office_version')
            indic_tool = request.POST.get('indic_tool')
            keyboard_type = request.POST.get('keyboard_type')
            mouse_type = request.POST.get('mouse_type')
            trellix_dlp_version = request.POST.get('trellix_dlp_version')
            trellix_version = request.POST.get('trellix_version')
            trellix_endpoint = request.POST.get('trellix_endpoint')
            trellix_threat = request.POST.get('trellix_threat')
            bigfix_control = request.POST.get('bigfix_control')
            pc_purpose = request.POST.get('pc_purpose')
            app_installed = request.POST.get('app_installed')
            floor = request.POST.get('floor')
            location_name = request.POST.get('location_name')
            
            printer_model = request.POST.get('printer_model')
            printer_serial_number = request.POST.get('printer_serial_number')
            printer_type = request.POST.get('printer_type')
            printer_status = request.POST.get('printer_status')
            printer_remark = request.POST.get('printer_remark')
            
            activity_1_status = request.POST.get('activity_1_status')
            activity_1_details = request.POST.get('activity_1_details')
            activity_2_status = request.POST.get('activity_2_status')
            activity_2_details = request.POST.get('activity_2_details')
            activity_3_status = request.POST.get('activity_3_status')
            activity_3_details = request.POST.get('activity_3_details')
            activity_4_status = request.POST.get('activity_4_status')
            activity_4_details = request.POST.get('activity_4_details')
            activity_5_status = request.POST.get('activity_5_status')
            activity_5_details = request.POST.get('activity_5_details')
            activity_6_status = request.POST.get('activity_6_status')
            activity_6_details = request.POST.get('activity_6_details')

            
            if not pm_no:
                quarter_mapping = {'q1': 1, 'q2': 2, 'q3': 3, 'q4': 4}
                pm_no = quarter_mapping.get(quarter.lower(), None)
            if not pm_no:
                messages.error(request, "PM No is required.")
                return render(request, 'maintenance_report_common.html', {'quarter': quarter})
            report = MaintenanceReport(
                pm_no=pm_no,
                quarter=quarter,
                date=date,
                year=year,
                cpu_make_model=cpu_make_model,
                serial_number=serial_number,
                computer_name=computer_name,
                employee_number= 'N/A' ,
                employee_name= 'N/A',
                employee_department= 'N/A',
                employee_designation= 'N/A',
                sro_tnso=sro_tnso,
                ip_address=ip_address,
                system_model=system_model,
                os_version=os_version,
                monitor_serial_number=monitor_serial_number,
                mouse_serial_number=mouse_serial_number,
                keyboard_serial_number=keyboard_serial_number,
                sap_version=sap_version,
                adobe_reader_version=adobe_reader_version,
                java_version=java_version,
                chrome_version=chrome_version,
                processor_type=processor_type,
                hdd_info=hdd_info,
                ram_info=ram_info,
                os_patch=os_patch,
                laps_version=laps_version,
                dsc_driver_version=dsc_driver_version,
                ms_office_version=ms_office_version,
                indic_tool=indic_tool,
                keyboard_type=keyboard_type,
                mouse_type=mouse_type,
                trellix_dlp_version=trellix_dlp_version,
                trellix_version=trellix_version,
                trellix_endpoint=trellix_endpoint,
                trellix_threat=trellix_threat,
                bigfix_control=bigfix_control,
                pc_purpose=pc_purpose,
                app_installed=app_installed,
                location_name=location_name,
                floor=floor,
                
                printer_model=printer_model,
                printer_serial_number=printer_serial_number,
                printer_type=printer_type,
                printer_status=printer_status,
                printer_remark=printer_remark,
                
                activity_1_status=activity_1_status,
                activity_1_details=activity_1_details,
                activity_2_status=activity_2_status,
                activity_2_details=activity_2_details,
                activity_3_status=activity_3_status,
                activity_3_details=activity_3_details,
                activity_4_status=activity_4_status,
                activity_4_details=activity_4_details,
                activity_5_status=activity_5_status,
                activity_5_details=activity_5_details,
                activity_6_status=activity_6_status,
                activity_6_details=activity_6_details,

            )
            report.save()
            return redirect('maintenance_report_success')
        quarter_mapping = {'q1': 1, 'q2': 2, 'q3': 3, 'q4': 4}
        pm_no = quarter_mapping.get(quarter.lower(), None)
        if pm_no is None:
            pm_no = "N/A"

        context = {
            'quarter': quarter,
            'pm_no': pm_no,
        }
        return render(request, 'maintenance_report_common.html', context)
    except Employee.DoesNotExist:
        return HttpResponse("Employee not found.", status=404)


def maintenance_report_success(request):
    return render(request, 'maintenance_report_success.html')


def get_system_info(request):
    hostname = platform.node()
    
    cpu_info = platform.processor()  # For CPU brand/model
    if not cpu_info:
        cpu_info = "Unknown CPU Info"

    try:
        if platform.system() == "Windows":
            system_model = subprocess.check_output("wmic computersystem get model", shell=True).decode().split('\n')[1].strip()
        elif platform.system() == "Darwin":  # macOS
            system_model = subprocess.check_output("system_profiler SPHardwareDataType | grep 'Model Identifier'", shell=True).decode().strip().split(":")[1].strip()
        else:
            system_model = subprocess.check_output("lshw -short | grep -i 'system'", shell=True).decode().split('\n')[0].strip()
    except Exception as e:
        system_model = "Unknown Model"


    # Get IP Address (first non-localhost address)
    ip_address = None
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET and addr.address != "127.0.0.1":
                ip_address = addr.address
                break
        if ip_address:
            break
        
    
    java_version = "Unknown Java Version"
    try:
        if platform.system() == "Windows":
            result = subprocess.run(["java", "-version"], capture_output=True, text=True)
        elif platform.system() == "Linux":
            result = subprocess.run(["java", "-version"], capture_output=True, text=True)
        if result.returncode == 0:
            # Extract Java version from the output
            java_version = result.stderr.split('\n')[0].strip().split('"')[1]
    except FileNotFoundError:
        java_version = "Java not installed"
        
    
    keyboard_serial_number = keyboard_serial()
    mouse_serial_number = mouse_serial()
    monitor_serial_number = monitor_serial()
    processor_type = get_processor_type()
    hdd_info = get_hdd_info()
    ram_info = get_ram_info()
    adobe_acrobat_version = get_adobe_acrobat_version()
    sap_version = get_sap_version()
    chrome_version = get_chrome_version()
    os_patch = get_os_patch()
    dsc_driver_version = get_dsc_driver_version()
    laps_version = get_laps_version()
    ms_office_version = get_office_version()
    indic_tool = check_indic_tool()
    keyboard_type = get_keyboard_type()
    mouse_type = get_mouse_type()
    serial_number = get_cpu_serial_number()
    trellix_dlp_version = get_trellix_dlp_version()
    trellix_version = get_trellix_agent_version()
    bigfix_control = get_bigfix_version()
    trellix_threat = get_trellix_threat()
    os_version = get_os_version()


    # Pack all information into a dictionary
    system_info = {
        "hostname": hostname,
        'cpuMakeModel': cpu_info,
        "serialNumber": serial_number,
        "ipAddress": ip_address,
        "systemModel": system_model,
        "mouseSerialNumber": mouse_serial_number,
        "keyboardSerialNumber": keyboard_serial_number,
        "monitorSerialNumber": monitor_serial_number,
        "osVersion": os_version,
        "processorType": processor_type,
        "ramInfo": ram_info,
        'hddInfo': hdd_info,
        'javaVersion': java_version,
        'chromeVersion': chrome_version,
        'sapVersion': sap_version,
        'adobeReaderVersion': adobe_acrobat_version,
        'osPatch' : os_patch,
        'msOfficeVersion': ms_office_version,
        'lapsVersion': laps_version,
        "dscDriverVersion": dsc_driver_version,
        "indicTool": indic_tool,
        "keyboardType": keyboard_type,
        "mouseType": mouse_type,
        "trellixDlpVersion": trellix_dlp_version,
        "trellixVersion": trellix_version,
        "bigfixControl": bigfix_control,
        "trellixThreat": trellix_threat,
    }
    return JsonResponse(system_info)


def get_os_version():
    os_version = platform.system() + " " + platform.release()
    if platform.system() == "Windows":
        try:
            pythoncom.CoInitialize()
            wmi = win32com.client.Dispatch("WbemScripting.SWbemLocator")
            namespace = wmi.ConnectServer(".", "root\\CIMV2")
            os_info = namespace.ExecQuery("SELECT * FROM Win32_OperatingSystem")
            for os in os_info:
                edition = os.Caption  # Full version string, e.g., "Microsoft Windows 10 Pro"
            edition = edition.split(' ')[-1]  # Get the last word (e.g., "Pro")
            os_version += " " + edition
            return os_version
        except Exception as e:
            print(f"Error getting full Windows version: {e}")
            return os_version
        finally:
            pythoncom.CoUninitialize()
    return os_version
# full_version = get_os_version()
# print(full_version)


def monitor_serial():
    try:
        result = subprocess.run(
            ['wmic', 'path', 'Win32_DesktopMonitor', 'get', 'PNPDeviceID'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            lines = result.stdout.splitlines()
            for line in lines[1:]:
                pnp_device_id = line.strip()
                if pnp_device_id:
                    monitor_serial = pnp_device_id.split("\\")[-1]
                    return monitor_serial
        return "Unknown Monitor Serial"
    except Exception as e:
        return f"Error fetching monitor serial: {str(e)}"
# print("Monitor Serial: ", monitor_serial())


def get_cpu_serial_number():
    try:
        pythoncom.CoInitialize()
        c = wmi.WMI()
        for bios in c.Win32_BIOS():
            return bios.SerialNumber
        return "Unknown BIOS Serial Number"
    except Exception as e:
        return f"Error fetching BIOS Serial: {str(e)}"
    finally:
        try:
            pythoncom.CoUninitialize()
        except Exception as cleanup_error:
            print(f"Error during COM uninitialization: {cleanup_error}")
# print(f"CPU Serial Number:", get_cpu_serial_number())



def keyboard_serial():
    try:
        result = subprocess.run(
            ['wmic', 'path', 'Win32_Keyboard', 'get', 'PNPDeviceID'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            lines = result.stdout.splitlines()
            for line in lines[1:]:
                pnp_device_id = line.strip()
                if pnp_device_id:
                    keyboard_serial = pnp_device_id.split("\\")[-1]
                    return keyboard_serial
        return "Unknown Keyboard Serial"
    except Exception as e:
        return f"Error fetching keyboard serial: {str(e)}"
# print("Keyboard Serial: ", keyboard_serial())


def mouse_serial():
    try:
        result = subprocess.run(
            ['wmic', 'path', 'Win32_PointingDevice', 'get', 'PNPDeviceID'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            lines = result.stdout.splitlines()
            for line in lines[1:]:
                pnp_device_id = line.strip()
                if pnp_device_id:
                    mouse_serial = pnp_device_id.split("\\")[-1]
                    return mouse_serial
        return "Unknown Mouse Serial"
    except Exception as e:
        return f"Error fetching mouse serial: {str(e)}"
# print("Mouse Serial: ", mouse_serial())


def get_processor_type():
    try:
        result = subprocess.run(
            ['wmic', 'cpu', 'get', 'Name'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            lines = result.stdout.splitlines()
            for line in lines[1:]:
                processor_name = line.strip()
                if processor_name:
                    return processor_name
        return "Unknown Processor Type"
    except Exception as e:
        return f"Error fetching processor type: {str(e)}"
# print("Processor Type: ", get_processor_type())


def get_hdd_info():
    try:
        result = subprocess.run(
            ['powershell', '-Command', 'Get-WmiObject -Class Win32_DiskDrive | Select-Object Model, Size, MediaType'],
            capture_output=True, text=True
        )
        if not result.stdout.strip():
            return "No output from PowerShell command. Please check system configuration."
        if result.returncode == 0:
            lines = result.stdout.splitlines()
            hdd_info = []
            for line in lines[3:]:
                line = line.strip()
                if line:
                    parts = line.split()
                    if len(parts) >= 3:
                        model = parts[0]
                        size_in_bytes = int(parts[1])
                        media_type = " ".join(parts[2:])
                        if size_in_bytes >= 1024**4:
                            size = size_in_bytes / (1024**4)
                            size_str = f"{size:.2f} TB"
                        else:
                            size = size_in_bytes / (1024**3)
                            size_str = f"{size:.2f} GB"
                        hdd_info.append(f"{size_str}/{model}")
            if hdd_info:
                return "\n".join(hdd_info)
            else:
                return "No HDD information found"
        return "Error fetching HDD information"
    except Exception as e:
        return f"Error fetching HDD information: {str(e)}"
# print("HDD Info: \n", get_hdd_info())


def get_ram_info():
    try:
        result = subprocess.run(
            ['powershell', '-Command', 'Get-WmiObject -Class Win32_PhysicalMemory | Select-Object Capacity'],
            capture_output=True, text=True
        )
        if not result.stdout.strip():
            return "No output from PowerShell command. Please check system configuration."
        if result.returncode == 0:
            lines = result.stdout.splitlines()
            ram_sizes = []
            total_capacity_bytes = 0
            for line in lines[3:]:
                line = line.strip()
                if line:
                    parts = line.split()
                    if len(parts) >= 1:
                        capacity_in_bytes = int(parts[0])
                        ram_sizes.append(capacity_in_bytes / (1024**3))
                        total_capacity_bytes += capacity_in_bytes
            ram_info_str = " / ".join([f"{size:.0f} GB" for size in ram_sizes])
            return f"{ram_info_str}"
        return "Error fetching RAM information"
    except Exception as e:
        return f"Error fetching RAM information: {str(e)}"
# print("RAM Info: \n", get_ram_info())


def get_chrome_version():
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if not os.path.exists(chrome_path):
        chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    if os.path.exists(chrome_path):
        version_info = os.popen(f'wmic datafile where name="{chrome_path.replace("\\", "\\\\")}" get Version').read().strip()
        return version_info.split("\n")[-1]  # Extract version number
    return "Chrome is not installed."
# print("Chrome Version: " + get_chrome_version())


def get_sap_version():
    sap_path = r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\sapgui.exe"
    if os.path.exists(sap_path):
        version_info = os.popen(f'wmic datafile where name="{sap_path.replace("\\", "\\\\")}" get Version').read().strip()
        return version_info.split("\n")[-1]  # Extract version number
    return "SAP GUI is not installed."
# print("SAP Version: " + get_sap_version())



def get_adobe_acrobat_version():
    try:
        registry_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]
        for registry_path in registry_paths:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path)
            num_subkeys = winreg.QueryInfoKey(key)[0]
            for i in range(num_subkeys):
                subkey_name = winreg.EnumKey(key, i)
                subkey = winreg.OpenKey(key, subkey_name)
                try:
                    display_name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                    if "Adobe Acrobat" in display_name:
                        version, _ = winreg.QueryValueEx(subkey, "DisplayVersion")
                        winreg.CloseKey(subkey)
                        return version
                except FileNotFoundError:
                    pass
                winreg.CloseKey(subkey)
        return "Adobe Acrobat is not installed or version info is missing."
    except Exception as e:
        return f"Error: {str(e)}"
# print("Adobe Acrobat: " + get_adobe_acrobat_version())


def get_os_patch():
    try:
        result = subprocess.run(
            ['wmic', 'os', 'get', 'BuildNumber'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            lines = result.stdout.splitlines()
            for line in lines[1:]:  # Starting from the second line (after the header)
                build_number = line.strip()  # Strip extra spaces
                if build_number:  # If the line is not empty
                    return build_number
            return "Unknown Build Number"
        return "Unknown Build Number"
    except Exception as e:
        return f"Error fetching build number: {str(e)}"
# print("OS Build Number: ", get_os_patch())


def get_laps_version():
    try:
        laps_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\LAPS"
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, laps_key)
        version, _ = winreg.QueryValueEx(key, "DisplayVersion")
        return version
    except WindowsError:
        return "LAPS not installed"
    
    
def get_office_version():
    try:
        office_path = r"C:\Program Files\Microsoft Office\Office16\winword.exe"
        if not os.path.exists(office_path):
            office_path = r"C:\Program Files (x86)\Microsoft Office\Office16\winword.exe"
        if os.path.exists(office_path):
            version_info = subprocess.check_output(
                f'wmic datafile where name="{office_path.replace("\\", "\\\\")}" get Version', shell=True
            ).decode().strip()
            version = version_info.split('\n')[-1].strip()
            major_version = version.split('.')[0]
            return f"Office {major_version}"
        return "Microsoft Office is not installed."
    except Exception as e:
        return f"Error: {str(e)}"
# print("microsoft version: " + get_office_version())


def get_dsc_driver_version():
    try:
        result = subprocess.check_output('wmic product where "name like \'%DSC%\'" get Name, Version', shell=True, text=True)
        if result:
            lines = result.strip().split('\n')
            for line in lines[1:]:
                if "DSC" in line:
                    parts = line.split()
                    version = parts[-1]
                    return version.strip()
        return "DSC Driver not found."
    except Exception as e:
        return f"Error fetching DSC Driver version: {str(e)}"
# print("DSC Driver Version: " + get_dsc_driver_version())


def check_indic_tool():
    try:
        installed_programs = subprocess.check_output(
            'wmic product get Name', shell=True, text=True
        )
        if "Microsoft Indic Language Input Tool" in installed_programs:
            return "Yes"
        else:
            return "No"
    except Exception as e:
        return f"Error checking for the Indic Language Input Tool: {str(e)}"
# print(check_indic_tool())


def get_keyboard_type():
    try:
        device_info = subprocess.check_output('wmic path Win32_Keyboard get PNPDeviceID', shell=True, text=True)
        if "USB" in device_info:
            return "Wired"
        elif "BTH" in device_info:
            return "Wireless (Bluetooth)"
        else:
            return "Unknown"
    except Exception as e:
        return f"Error checking keyboard: {str(e)}"
# print(f"Keyboard Type:", get_keyboard_type())


def get_mouse_type():
    try:
        device_info = subprocess.check_output('wmic path Win32_PointingDevice get PNPDeviceID', shell=True, text=True)
        if "USB" in device_info:
            return "Wired"
        elif "BTH" in device_info:
            return "Wireless (Bluetooth)"
        else:
            return "Unknown"
    except Exception as e:
        return f"Error checking mouse: {str(e)}"
# print(f"Mouse Type:", get_mouse_type())


def get_trellix_dlp_version():
    try:
        result = subprocess.check_output('wmic product where "name like \'%Trellix%\' or name like \'%McAfee%\'" get Name, Version', shell=True, text=True)
        if result:
            lines = result.strip().split('\n')
            for line in lines[1:]:
                if "Trellix" in line or "McAfee" in line:
                    parts = line.split()
                    version = parts[-1]
                    return version.strip()
        return "Trellix Agent not found."
    except Exception as e:
        return f"Error fetching Trellix Agent version: {str(e)}"
# print(get_trellix_dlp_version())


def get_trellix_agent_version():
    try:
        result = subprocess.check_output('wmic product where "name like \'%Trellix Agent%\' or name like \'%McAfee%\'" get Name, Version', shell=True, text=True)
        
        if result:
            lines = result.strip().split('\n')
            for line in lines[1:]:
                if "Trellix Agent" in line:
                    parts = line.split()
                    version = parts[-1]
                    return version.strip()
        return "Trellix Agent not found."
    except Exception as e:
        return f"Error fetching Trellix Agent version: {str(e)}"
# print(get_trellix_agent_version())



def get_bigfix_version():
    try:
        command = 'wmic product where "name like \'BigFix%\'" get version'
        output = subprocess.check_output(command, shell=True, text=True)
        version = output.strip().split("\n")[-1]
        return version
    except Exception as e:
        return f"Error retrieving BigFix version using WMIC: {str(e)}"
# print(get_bigfix_version())


def get_trellix_endpoint():
    try:
        command = 'wmic product where "name like \'%Trellix Endpoint Security%\'" get name, version'
        output = subprocess.check_output(command, shell=True, text=True)
        output_lines = output.strip().split("\n")
        if len(output_lines) > 1:
            for line in output_lines[1:]:
                if "Trellix Endpoint Security" in line:
                    version = line.strip().split()[-1]
                    return version
            return "Product found, but no version detected."
        else:
            return "Version not found"
    except Exception as e:
        return f"Error retrieving Trellix version using WMIC: {str(e)}"
# print(get_trellix_endpoint())


    
def get_trellix_threat():
    try:
        command = 'wmic product get name'
        output = subprocess.check_output(command, shell=True, text=True)

        if "McAfee" in output or "Trellix" in output:
            return "Yes"
        else:
            return "No"
    except Exception as e:
        return f"Error checking for Trellix: {str(e)}"
# print(get_trellix_threat())
    
    
# def get_ultravnc_version():
#     ultravnc_path = r"C:\Program Files (x86)\UltraVNC\vncviewer.exe"
#     if os.path.exists(ultravnc_path):
#         version_info = os.popen(f'wmic datafile where name="{ultravnc_path.replace("\\", "\\\\")}" get Version').read().strip()
#         return version_info.split("\n")[-1]  # Extract version number
#     return "UltraVNC is not installed."
# # print("Ultra VNC Version: " + get_ultravnc_version())
