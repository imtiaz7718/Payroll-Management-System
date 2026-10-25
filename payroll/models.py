from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta

# Department Model
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


# Enhanced Employee Model
class Employee(models.Model):
    POSITION = [
        ("Junior", "Junior"),
        ("Senior", "Senior"),
        ("Manager", "Manager"),
        ("Director", "Director"),
    ]
    
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("On Leave", "On Leave"),
    ]

    # Basic Info
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    
    # Employment Details
    employee_id = models.CharField(max_length=20, unique=True)
    position = models.CharField(max_length=20, choices=POSITION)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    experience = models.IntegerField()
    base_salary = models.FloatField()
    
    # Address
    address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    
    # Tax & Bank Details
    pan = models.CharField(max_length=20, blank=True)
    aadhar = models.CharField(max_length=20, blank=True)
    bank_account = models.CharField(max_length=20, blank=True)
    ifsc_code = models.CharField(max_length=20, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Active")
    date_joined = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['employee_id']),
            models.Index(fields=['status']),
        ]

    def save(self, *args, **kwargs):
        """Auto-generate employee_id if not provided"""
        if not self.employee_id:
            # Generate employee_id: EMP001, EMP002, etc.
            last_employee = Employee.objects.all().order_by('-id').first()
            if last_employee:
                last_id = int(last_employee.employee_id.replace('EMP', ''))
                self.employee_id = f"EMP{last_id + 1:03d}"
            else:
                self.employee_id = "EMP001"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.employee_id})"


# Attendance Model
class Attendance(models.Model):
    ATTENDANCE_STATUS = [
        ("Present", "Present"),
        ("Absent", "Absent"),
        ("Leave", "Leave"),
        ("Half Day", "Half Day"),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('employee', 'date')
        ordering = ['-date']


# Salary Structure Model
class SalaryStructure(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='salary_structure')
    base_salary = models.FloatField()
    dearness_allowance = models.FloatField(default=0)
    house_rent_allowance = models.FloatField(default=0)
    medical_allowance = models.FloatField(default=0)
    conveyance_allowance = models.FloatField(default=0)
    other_allowances = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def gross_salary(self):
        return (self.base_salary + self.dearness_allowance + self.house_rent_allowance + 
                self.medical_allowance + self.conveyance_allowance + self.other_allowances)
    
    def __str__(self):
        return f"{self.employee.name} - Salary Structure"


# Deductions Model
class Deduction(models.Model):
    DEDUCTION_TYPE = [
        ("Income Tax", "Income Tax"),
        ("PF", "Provident Fund"),
        ("ESI", "Employee State Insurance"),
        ("Health Insurance", "Health Insurance"),
        ("Professional Tax", "Professional Tax"),
        ("Loan", "Loan"),
        ("Other", "Other"),
    ]
    
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='deductions')
    income_tax = models.FloatField(default=0)
    provident_fund = models.FloatField(default=0)
    esi = models.FloatField(default=0)
    health_insurance = models.FloatField(default=0)
    professional_tax = models.FloatField(default=0)
    loan_amount = models.FloatField(default=0)
    other_deductions = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def total_deductions(self):
        return (self.income_tax + self.provident_fund + self.esi + 
                self.health_insurance + self.professional_tax + self.loan_amount + self.other_deductions)
    
    def __str__(self):
        return f"{self.employee.name} - Deductions"


# Payroll Model
class Payroll(models.Model):
    STATUS_CHOICES = [
        ("Draft", "Draft"),
        ("Processed", "Processed"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payrolls')
    month = models.IntegerField()  # 1-12
    year = models.IntegerField()
    
    # Attendance
    days_worked = models.FloatField(default=0)
    total_days = models.FloatField(default=30)
    
    # Earnings
    gross_salary = models.FloatField()
    basic_salary = models.FloatField()
    allowances = models.FloatField(default=0)
    
    # Deductions
    total_deductions = models.FloatField(default=0)
    
    # Final
    net_salary = models.FloatField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Draft")
    process_date = models.DateTimeField(blank=True, null=True)
    approved_by = models.CharField(max_length=100, blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('employee', 'month', 'year')
        ordering = ['-year', '-month']
    
    def __str__(self):
        return f"{self.employee.name} - {self.month}/{self.year}"


# Payslip Model
class Payslip(models.Model):
    payroll = models.OneToOneField(Payroll, on_delete=models.CASCADE, related_name='payslip')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payslips')
    
    generated_date = models.DateTimeField(auto_now_add=True)
    payslip_number = models.CharField(max_length=50, unique=True)
    
    # Detailed components
    basic_salary = models.FloatField()
    allowances = models.FloatField()
    gross_salary = models.FloatField()
    
    income_tax = models.FloatField(default=0)
    provident_fund = models.FloatField(default=0)
    esi = models.FloatField(default=0)
    other_deductions = models.FloatField(default=0)
    total_deductions = models.FloatField()
    
    net_salary = models.FloatField()
    
    def __str__(self):
        return f"Payslip - {self.payslip_number}"


# Report Model
class PayrollReport(models.Model):
    REPORT_TYPE = [
        ("Monthly", "Monthly"),
        ("Quarterly", "Quarterly"),
        ("Annual", "Annual"),
        ("Custom", "Custom"),
    ]
    
    name = models.CharField(max_length=100)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE)
    month_from = models.IntegerField()
    month_to = models.IntegerField()
    year = models.IntegerField()
    
    total_employees = models.IntegerField()
    total_gross_salary = models.FloatField()
    total_deductions = models.FloatField()
    total_net_salary = models.FloatField()
    
    generated_date = models.DateTimeField(auto_now_add=True)
    generated_by = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} - {self.report_type}"
