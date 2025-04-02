from django.db import migrations, models
from django.contrib.auth.hashers import make_password

def set_default_password(apps, schema_editor):
    Employee = apps.get_model('report', 'Employee')  # Ensure the correct app name is used
    common_password = "Cipl@123"  # Default password
    hashed_password = make_password(common_password)
    
    # Update the password field for all employees
    Employee.objects.update(password=hashed_password)

class Migration(migrations.Migration):

    dependencies = [
        ('report', '0025_alter_employee_employee_number'),  # Your last migration file
    ]

    operations = [
        migrations.RunPython(set_default_password),
    ]
