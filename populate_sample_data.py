#!/usr/bin/env python
"""
Script to populate sample data into the Payroll Management System
Usage: python populate_sample_data.py
"""

import json
import os
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payroll_project.settings')
django.setup()

from payroll.models import Department, Employee, Attendance, SalaryStructure, Deduction

def load_sample_data():
    print("🚀 Starting sample data population...")
    
    # Load JSON data
    with open('sample_data.json', 'r') as f:
        data = json.load(f)
    
    # Create Departments
    print("\n📁 Creating departments...")
    departments = {}
    for dept_data in data['departments']:
        dept, created = Department.objects.get_or_create(
            name=dept_data['name'],
            defaults={'description': dept_data['description']}
        )
        departments[dept_data['name']] = dept
        status = "✅ Created" if created else "⏭️ Already exists"
        print(f"   {status}: {dept.name}")
    
    # Create Employees with related data
    print("\n👥 Creating employees...")
    for emp_data in data['employees']:
        # Get department
        department = departments.get(emp_data['department'])
        if not department:
            print(f"   ❌ Department not found for {emp_data['first_name']}")
            continue
        
        # Create employee
        employee, created = Employee.objects.get_or_create(
            email=emp_data['email'],
            defaults={
                'name': f"{emp_data['first_name']} {emp_data['last_name']}",
                'phone': emp_data['phone'],
                'position': emp_data['position'],
                'department': department,
                'experience': emp_data['experience'],
                'base_salary': emp_data['base_salary'],
                'address': emp_data['address'],
                'city': emp_data['city'],
                'state': emp_data['state'],
                'zip_code': emp_data['zip_code'],
                'pan': emp_data['pan'],
                'aadhar': emp_data['aadhar'],
                'bank_account': emp_data['bank_account'],
                'ifsc_code': emp_data['ifsc_code'],
                'status': 'Active',
                'date_joined': datetime.now().date()
            }
        )
        
        if created:
            # Create Salary Structure
            SalaryStructure.objects.get_or_create(
                employee=employee,
                defaults={
                    'base_salary': emp_data['base_salary'],
                    'dearness_allowance': emp_data['base_salary'] * 0.15,
                    'house_rent_allowance': emp_data['base_salary'] * 0.25,
                    'medical_allowance': 5000,
                    'conveyance_allowance': 3000,
                    'other_allowances': 2000
                }
            )
            
            # Create Deductions
            Deduction.objects.get_or_create(
                employee=employee,
                defaults={
                    'income_tax': emp_data['base_salary'] * 0.10,
                    'provident_fund': emp_data['base_salary'] * 0.12,
                    'esi': emp_data['base_salary'] * 0.02,
                    'health_insurance': 500,
                    'professional_tax': 200,
                    'loan_amount': 0,
                    'other_deductions': 0
                }
            )
            
            print(f"   ✅ Created: {employee.name} ({employee.position})")
        else:
            print(f"   ⏭️ Already exists: {employee.name}")
    
    # Create sample attendance for last 30 days
    print("\n📅 Creating sample attendance records...")
    attendances_created = 0
    employees = Employee.objects.filter(status='Active')
    
    for i in range(30):
        date = datetime.now().date() - timedelta(days=i)
        # Skip weekends
        if date.weekday() >= 5:
            continue
        
        for employee in employees:
            # 80% present, 15% absent, 5% leave
            import random
            rand = random.random()
            if rand < 0.80:
                status = 'Present'
            elif rand < 0.95:
                status = 'Absent'
            else:
                status = 'Leave'
            
            attendance, created = Attendance.objects.get_or_create(
                employee=employee,
                date=date,
                defaults={'status': status, 'remarks': 'Sample attendance record'}
            )
            
            if created:
                attendances_created += 1
    
    print(f"   ✅ Created {attendances_created} attendance records")
    
    print("\n" + "="*50)
    print("✨ Sample data successfully populated!")
    print("="*50)
    print("\n📊 Summary:")
    print(f"   • Departments: {Department.objects.count()}")
    print(f"   • Employees: {Employee.objects.count()}")
    print(f"   • Salary Structures: {SalaryStructure.objects.count()}")
    print(f"   • Deductions: {Deduction.objects.count()}")
    print(f"   • Attendance Records: {Attendance.objects.count()}")
    print("\n💡 Next steps:")
    print("   1. Create superuser: python manage.py createsuperuser")
    print("   2. Run migrations: python manage.py migrate")
    print("   3. Start server: python manage.py runserver")
    print("   4. Access: http://localhost:8000/login/")

if __name__ == '__main__':
    try:
        load_sample_data()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
