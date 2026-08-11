from django.contrib import admin
from .models import (Employee, Department, Attendance, SalaryStructure, 
                     Deduction, Payroll, Payslip, PayrollReport)

# Department Admin
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


# Employee Admin
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'name', 'position', 'department', 'status', 'created_at')
    list_filter = ('position', 'status', 'department', 'created_at')
    search_fields = ('name', 'employee_id', 'email')
    readonly_fields = ('employee_id', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'email', 'phone', 'employee_id')
        }),
        ('Employment Details', {
            'fields': ('position', 'department', 'experience', 'base_salary', 'date_joined', 'status')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'zip_code')
        }),
        ('Tax & Bank Details', {
            'fields': ('pan', 'aadhar', 'bank_account', 'ifsc_code')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Attendance Admin
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'status', 'created_at')
    list_filter = ('status', 'date')
    search_fields = ('employee__name', 'employee__employee_id')
    date_hierarchy = 'date'


# Salary Structure Admin
@admin.register(SalaryStructure)
class SalaryStructureAdmin(admin.ModelAdmin):
    list_display = ('employee', 'base_salary', 'gross_salary', 'updated_at')
    search_fields = ('employee__name', 'employee__employee_id')
    readonly_fields = ('created_at', 'updated_at')


# Deduction Admin
@admin.register(Deduction)
class DeductionAdmin(admin.ModelAdmin):
    list_display = ('employee', 'total_deductions', 'updated_at')
    search_fields = ('employee__name', 'employee__employee_id')
    readonly_fields = ('created_at', 'updated_at')


# Payroll Admin
@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee', 'month', 'year', 'gross_salary', 'net_salary', 'status')
    list_filter = ('status', 'month', 'year')
    search_fields = ('employee__name', 'employee__employee_id')
    readonly_fields = ('created_at', 'updated_at')


# Payslip Admin
@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = ('payslip_number', 'employee', 'net_salary', 'generated_date')
    search_fields = ('payslip_number', 'employee__name', 'employee__employee_id')
    readonly_fields = ('payslip_number', 'generated_date')


# Payroll Report Admin
@admin.register(PayrollReport)
class PayrollReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'report_type', 'total_net_salary', 'generated_date')
    list_filter = ('report_type', 'generated_date')
    search_fields = ('name', 'generated_by')
    readonly_fields = ('generated_date',)
