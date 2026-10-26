from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Employee Management
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('employees/<int:emp_id>/', views.employee_detail, name='employee_detail'),
    path('employees/<int:emp_id>/edit/', views.edit_employee, name='edit_employee'),
    path('employees/<int:emp_id>/delete/', views.delete_employee, name='delete_employee'),
    
    # Attendance Management
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    
    # Salary Structure
    path('salary-structure/', views.salary_structure_list, name='salary_structure_list'),
    path('salary-structure/<int:emp_id>/', views.salary_structure_detail, name='salary_structure_detail'),
    path('salary-structure/<int:emp_id>/edit/', views.edit_salary_structure, name='edit_salary_structure'),
    
    # Deductions
    path('deductions/', views.deduction_list, name='deduction_list'),
    path('deductions/<int:emp_id>/edit/', views.edit_deductions, name='edit_deductions'),
    
    # Payroll Processing
    path('payroll/', views.payroll_list, name='payroll_list'),
    path('payroll/process/', views.process_payroll, name='process_payroll'),
    
    # Payslips
    path('payslips/', views.payslip_list, name='payslip_list'),
    path('payslips/<int:payroll_id>/generate/', views.generate_payslip, name='generate_payslip'),
    path('payslips/<int:payslip_id>/pdf/', views.payslip_pdf, name='payslip_pdf'),
    
    # Reports
    path('reports/', views.report_list, name='report_list'),
    path('reports/generate/', views.generate_report, name='generate_report'),
    path('reports/<int:report_id>/', views.report_detail, name='report_detail'),
]
