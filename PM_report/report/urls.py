from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.choice_page, name='choice_page'),
    path('login/', views.login_view, name='login_view'),
    path('quarter-selection/', views.quarter_selection, name='quarter_selection'),
    path('employee/<str:employee_number>/', views.employee_details, name='employee_details'),
    path('api/system-info', views.get_system_info, name='get_system_info'),
    path('maintenance_report_success/', views.maintenance_report_success, name='maintenance_report_success'),
    path('maintenance-report/<str:employee_number>/<str:quarter>/', views.maintenance_report, name='maintenance_report'),
    path('maintenance-report-commmon/<str:quarter>/', views.maintenance_report_common, name='maintenance_report_common'),

    path('view-report/', views.view_report, name='view_report'),
    path('validate_password/<str:employee_number>/', views.validate_password, name='validate_password'),
]
