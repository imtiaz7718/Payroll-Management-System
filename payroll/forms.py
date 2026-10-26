from django import forms
from django.core.exceptions import ValidationError
from .models import Employee, Department, Attendance, SalaryStructure, Deduction, Payroll

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'email', 'phone', 'position', 'department', 'experience', 
                  'base_salary', 'address', 'city', 'state', 'zip_code', 'pan', 
                  'aadhar', 'bank_account', 'ifsc_code', 'date_joined', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'position': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Years of Experience'}),
            'base_salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Base Salary'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
            'pan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PAN'}),
            'aadhar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Aadhar'}),
            'bank_account': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bank Account'}),
            'ifsc_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'IFSC Code'}),
            'date_joined': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class SalaryStructureForm(forms.ModelForm):
    class Meta:
        model = SalaryStructure
        fields = ['base_salary', 'dearness_allowance', 'house_rent_allowance', 
                  'medical_allowance', 'conveyance_allowance', 'other_allowances']
        widgets = {
            'base_salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'dearness_allowance': forms.NumberInput(attrs={'class': 'form-control'}),
            'house_rent_allowance': forms.NumberInput(attrs={'class': 'form-control'}),
            'medical_allowance': forms.NumberInput(attrs={'class': 'form-control'}),
            'conveyance_allowance': forms.NumberInput(attrs={'class': 'form-control'}),
            'other_allowances': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class DeductionForm(forms.ModelForm):
    class Meta:
        model = Deduction
        fields = ['income_tax', 'provident_fund', 'esi', 'health_insurance', 
                  'professional_tax', 'loan_amount', 'other_deductions']
        widgets = {
            'income_tax': forms.NumberInput(attrs={'class': 'form-control'}),
            'provident_fund': forms.NumberInput(attrs={'class': 'form-control'}),
            'esi': forms.NumberInput(attrs={'class': 'form-control'}),
            'health_insurance': forms.NumberInput(attrs={'class': 'form-control'}),
            'professional_tax': forms.NumberInput(attrs={'class': 'form-control'}),
            'loan_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'other_deductions': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['date', 'status', 'remarks']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = ['month', 'year', 'days_worked', 'total_days']
        widgets = {
            'month': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'days_worked': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.5}),
            'total_days': forms.NumberInput(attrs={'class': 'form-control'}),
        }
