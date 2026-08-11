from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Sum, Count, Q, F, Value, FloatField
from django.db.models.functions import Coalesce
from django.utils import timezone
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from io import BytesIO
import json

from .models import (Employee, Department, Attendance, SalaryStructure, 
                     Deduction, Payroll, Payslip, PayrollReport)

# ============= DASHBOARD VIEW =============
@login_required
def dashboard(request):
    """Main dashboard with overview statistics and charts"""
    
    # Employee Statistics
    total_employees = Employee.objects.filter(status='Active').count()
    total_on_leave = Employee.objects.filter(status='On Leave').count()
    total_inactive = Employee.objects.filter(status='Inactive').count()
    
    # Position-wise distribution
    juniors = Employee.objects.filter(position='Junior', status='Active').count()
    seniors = Employee.objects.filter(position='Senior', status='Active').count()
    managers = Employee.objects.filter(position='Manager', status='Active').count()
    directors = Employee.objects.filter(position='Director', status='Active').count()
    
    # Department-wise distribution
    departments = Department.objects.annotate(
        emp_count=Count('employee')
    ).values('name', 'emp_count')
    
    # Attendance statistics for current date
    today = timezone.now().date()
    present_today = Attendance.objects.filter(
        date=today, 
        status='Present'
    ).count()
    absent_today = Attendance.objects.filter(
        date=today, 
        status='Absent'
    ).count()
    leave_today = Attendance.objects.filter(
        date=today, 
        status='Leave'
    ).count()
    
    # Salary statistics
    total_gross_salary = SalaryStructure.objects.aggregate(
        total=Coalesce(Sum('base_salary', output_field=FloatField()), Value(0.0, output_field=FloatField()))
    )['total']
    
    # Recent payrolls
    recent_payrolls = Payroll.objects.select_related('employee').order_by('-created_at')[:5]
    
    # Recent payslips
    recent_payslips = Payslip.objects.select_related('employee').order_by('-generated_date')[:5]
    
    context = {
        'total_employees': total_employees,
        'total_on_leave': total_on_leave,
        'total_inactive': total_inactive,
        'total_gross_salary': total_gross_salary,
        'position_data': [juniors, seniors, managers, directors],
        'position_labels': ['Junior', 'Senior', 'Manager', 'Director'],
        'present_today': present_today,
        'absent_today': absent_today,
        'leave_today': leave_today,
        'departments': list(departments),
        'recent_payrolls': recent_payrolls,
        'recent_payslips': recent_payslips,
    }
    
    return render(request, 'dashboard.html', context)


# ============= EMPLOYEE MANAGEMENT VIEWS =============
@login_required
def employee_list(request):
    """List all employees with filters"""
    
    employees = Employee.objects.select_related('department').all()
    
    # Filters
    status_filter = request.GET.get('status')
    position_filter = request.GET.get('position')
    department_filter = request.GET.get('department')
    search = request.GET.get('search')
    
    if status_filter:
        employees = employees.filter(status=status_filter)
    if position_filter:
        employees = employees.filter(position=position_filter)
    if department_filter:
        employees = employees.filter(department_id=department_filter)
    if search:
        employees = employees.filter(
            Q(name__icontains=search) | 
            Q(employee_id__icontains=search) |
            Q(email__icontains=search)
        )
    
    departments = Department.objects.all()
    
    context = {
        'employees': employees,
        'departments': departments,
        'current_status': status_filter,
        'current_position': position_filter,
        'current_department': department_filter,
        'search_query': search,
    }
    
    return render(request, 'employees/employee_list.html', context)


@login_required
def employee_detail(request, emp_id):
    """View detailed employee information"""
    
    employee = get_object_or_404(Employee, id=emp_id)
    salary_structure = getattr(employee, 'salary_structure', None)
    deductions = getattr(employee, 'deductions', None)
    attendance_month = Attendance.objects.filter(employee=employee).last()
    recent_payslips = employee.payslips.all()[:6]
    
    context = {
        'employee': employee,
        'salary_structure': salary_structure,
        'deductions': deductions,
        'recent_payslips': recent_payslips,
    }
    
    return render(request, 'employees/employee_detail.html', context)


@login_required
def add_employee(request):
    """Add new employee"""
    
    if request.method == 'POST':
        try:
            # Generate employee ID
            last_emp = Employee.objects.order_by('-id').first()
            emp_id = f"EMP{1001 + (last_emp.id if last_emp else 0)}"
            
            # Create employee
            employee = Employee.objects.create(
                name=request.POST['name'],
                email=request.POST['email'],
                phone=request.POST.get('phone', ''),
                employee_id=emp_id,
                position=request.POST['position'],
                department_id=request.POST['department'],
                experience=int(request.POST['experience']),
                base_salary=float(request.POST['base_salary']),
                address=request.POST.get('address', ''),
                city=request.POST.get('city', ''),
                state=request.POST.get('state', ''),
                zip_code=request.POST.get('zip_code', ''),
                pan=request.POST.get('pan', ''),
                aadhar=request.POST.get('aadhar', ''),
                bank_account=request.POST.get('bank_account', ''),
                ifsc_code=request.POST.get('ifsc_code', ''),
                date_joined=request.POST.get('date_joined', timezone.now().date()),
                status='Active'
            )
            
            # Create default salary structure
            SalaryStructure.objects.create(
                employee=employee,
                base_salary=float(request.POST['base_salary']),
                dearness_allowance=float(request.POST.get('dearness_allowance', 0)),
                house_rent_allowance=float(request.POST.get('house_rent_allowance', 0)),
            )
            
            # Create default deductions
            Deduction.objects.create(
                employee=employee,
                income_tax=float(request.POST.get('income_tax', 0)),
                provident_fund=float(request.POST.get('provident_fund', 0)),
            )
            
            return redirect('employee_detail', emp_id=employee.id)
        except Exception as e:
            error = str(e)
            context = {'error': error, 'departments': Department.objects.all()}
            return render(request, 'employees/add_employee.html', context)
    
    departments = Department.objects.all()
    context = {'departments': departments}
    
    return render(request, 'employees/add_employee.html', context)


@login_required
def edit_employee(request, emp_id):
    """Edit employee information"""
    
    employee = get_object_or_404(Employee, id=emp_id)
    
    if request.method == 'POST':
        employee.name = request.POST.get('name', employee.name)
        employee.email = request.POST.get('email', employee.email)
        employee.phone = request.POST.get('phone', employee.phone)
        employee.position = request.POST.get('position', employee.position)
        employee.department_id = request.POST.get('department', employee.department_id)
        employee.experience = int(request.POST.get('experience', employee.experience))
        employee.base_salary = float(request.POST.get('base_salary', employee.base_salary))
        employee.address = request.POST.get('address', employee.address)
        employee.city = request.POST.get('city', employee.city)
        employee.state = request.POST.get('state', employee.state)
        employee.status = request.POST.get('status', employee.status)
        
        employee.save()
        
        return redirect('employee_detail', emp_id=employee.id)
    
    departments = Department.objects.all()
    context = {
        'employee': employee,
        'departments': departments,
    }
    
    return render(request, 'employees/edit_employee.html', context)


@login_required
def delete_employee(request, emp_id):
    """Delete employee"""
    
    employee = get_object_or_404(Employee, id=emp_id)
    
    if request.method == 'POST':
        employee.status = 'Inactive'
        employee.save()
        return redirect('employee_list')
    
    return render(request, 'employees/confirm_delete.html', {'employee': employee})


# ============= ATTENDANCE MANAGEMENT VIEWS =============
@login_required
def attendance_list(request):
    """View attendance records"""
    
    # Get current month and year or from request
    today = timezone.now().date()
    month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))
    
    # Get employees
    employees = Employee.objects.filter(status='Active')
    
    # Get attendance for the month
    attendance_records = Attendance.objects.filter(
        date__month=month,
        date__year=year
    ).select_related('employee')
    
    # Calculate statistics
    stats = attendance_records.aggregate(
        present=Count('id', filter=Q(status='Present')),
        absent=Count('id', filter=Q(status='Absent')),
        leave=Count('id', filter=Q(status='Leave')),
        half_day=Count('id', filter=Q(status='Half Day')),
    )
    
    context = {
        'employees': employees,
        'attendance_records': attendance_records,
        'month': month,
        'year': year,
        'stats': stats,
    }
    
    return render(request, 'attendance/attendance_list.html', context)


@login_required
@login_required
def mark_attendance(request):
    """Mark daily attendance"""
    
    if request.method == 'POST':
        today = timezone.now().date()
        
        for key, status in request.POST.items():
            if key.startswith('emp_'):
                emp_id = int(key.replace('emp_', ''))
                if status:  # Only save if status is selected
                    try:
                        employee = Employee.objects.get(id=emp_id)
                        Attendance.objects.update_or_create(
                            employee=employee,
                            date=today,
                            defaults={'status': status}
                        )
                    except Employee.DoesNotExist:
                        pass
        
        return redirect('attendance_list')
    
    today = timezone.now().date()
    employees = Employee.objects.filter(status='Active')
    
    # Get today's attendance records
    today_attendance_records = Attendance.objects.filter(date=today).values('employee_id', 'status')
    today_attendance = {att['employee_id']: att['status'] for att in today_attendance_records}
    
    context = {
        'employees': employees,
        'today_attendance': today_attendance,
        'date': today,
    }
    
    return render(request, 'attendance/mark_attendance.html', context)


# ============= SALARY STRUCTURE VIEWS =============
@login_required
def salary_structure_list(request):
    """View all salary structures"""
    
    salary_structures = SalaryStructure.objects.select_related('employee')
    
    context = {
        'salary_structures': salary_structures,
    }
    
    return render(request, 'salary/salary_structure_list.html', context)


@login_required
def salary_structure_detail(request, emp_id):
    """View detailed salary structure"""
    
    employee = get_object_or_404(Employee, id=emp_id)
    salary_structure, created = SalaryStructure.objects.get_or_create(employee=employee)
    
    context = {
        'employee': employee,
        'salary_structure': salary_structure,
    }
    
    return render(request, 'salary/salary_structure_detail.html', context)


@login_required
def edit_salary_structure(request, emp_id):
    """Edit salary structure"""
    
    employee = get_object_or_404(Employee, id=emp_id)
    salary_structure, created = SalaryStructure.objects.get_or_create(employee=employee)
    
    if request.method == 'POST':
        salary_structure.base_salary = float(request.POST.get('base_salary', 0))
        salary_structure.dearness_allowance = float(request.POST.get('dearness_allowance', 0))
        salary_structure.house_rent_allowance = float(request.POST.get('house_rent_allowance', 0))
        salary_structure.medical_allowance = float(request.POST.get('medical_allowance', 0))
        salary_structure.conveyance_allowance = float(request.POST.get('conveyance_allowance', 0))
        salary_structure.other_allowances = float(request.POST.get('other_allowances', 0))
        salary_structure.save()
        
        return redirect('salary_structure_detail', emp_id=emp_id)
    
    context = {
        'employee': employee,
        'salary_structure': salary_structure,
    }
    
    return render(request, 'salary/edit_salary_structure.html', context)


# ============= DEDUCTION VIEWS =============
@login_required
def deduction_list(request):
    """View all deductions"""
    
    deductions = Deduction.objects.select_related('employee')
    
    context = {
        'deductions': deductions,
    }
    
    return render(request, 'deductions/deduction_list.html', context)


@login_required
def edit_deductions(request, emp_id):
    """Edit employee deductions"""
    
    employee = get_object_or_404(Employee, id=emp_id)
    deduction, created = Deduction.objects.get_or_create(employee=employee)
    
    if request.method == 'POST':
        deduction.income_tax = float(request.POST.get('income_tax', 0))
        deduction.provident_fund = float(request.POST.get('provident_fund', 0))
        deduction.esi = float(request.POST.get('esi', 0))
        deduction.health_insurance = float(request.POST.get('health_insurance', 0))
        deduction.professional_tax = float(request.POST.get('professional_tax', 0))
        deduction.loan_amount = float(request.POST.get('loan_amount', 0))
        deduction.other_deductions = float(request.POST.get('other_deductions', 0))
        deduction.save()
        
        return redirect('deduction_list')
    
    context = {
        'employee': employee,
        'deduction': deduction,
    }
    
    return render(request, 'deductions/edit_deductions.html', context)


# ============= PAYROLL PROCESSING VIEWS =============
@login_required
def payroll_list(request):
    """View all payroll records"""
    
    month = int(request.GET.get('month', timezone.now().month))
    year = int(request.GET.get('year', timezone.now().year))
    status = request.GET.get('status')
    
    payrolls = Payroll.objects.select_related('employee').filter(month=month, year=year)
    
    if status:
        payrolls = payrolls.filter(status=status)
    
    # Calculate totals
    totals = payrolls.aggregate(
        total_gross=Coalesce(Sum('gross_salary', output_field=FloatField()), Value(0.0, output_field=FloatField())),
        total_deductions=Coalesce(Sum('total_deductions', output_field=FloatField()), Value(0.0, output_field=FloatField())),
        total_net=Coalesce(Sum('net_salary', output_field=FloatField()), Value(0.0, output_field=FloatField())),
    )
    
    context = {
        'payrolls': payrolls,
        'month': month,
        'year': year,
        'totals': totals,
        'current_status': status,
    }
    
    return render(request, 'payroll/payroll_list.html', context)


@login_required
def process_payroll(request):
    """Process payroll for selected month/year"""
    
    if request.method == 'POST':
        month = int(request.POST.get('month'))
        year = int(request.POST.get('year'))
        
        # Get all active employees
        employees = Employee.objects.filter(status='Active')
        
        for employee in employees:
            # Get attendance data
            attendance_data = Attendance.objects.filter(
                employee=employee,
                date__month=month,
                date__year=year
            )
            
            present_days = attendance_data.filter(status='Present').count()
            half_days = attendance_data.filter(status='Half Day').count()
            days_worked = present_days + (half_days * 0.5)
            
            # Get salary structure
            salary_structure = getattr(employee, 'salary_structure', None)
            if not salary_structure:
                continue
            
            gross_salary = salary_structure.gross_salary()
            basic_salary = salary_structure.base_salary
            
            # Calculate deductions
            deduction = getattr(employee, 'deductions', None)
            if deduction:
                total_deductions = deduction.total_deductions()
            else:
                total_deductions = 0
            
            # Calculate net salary
            net_salary = gross_salary - total_deductions
            
            # Create or update payroll
            payroll, created = Payroll.objects.update_or_create(
                employee=employee,
                month=month,
                year=year,
                defaults={
                    'days_worked': days_worked,
                    'total_days': 30,
                    'gross_salary': gross_salary,
                    'basic_salary': basic_salary,
                    'allowances': gross_salary - basic_salary,
                    'total_deductions': total_deductions,
                    'net_salary': net_salary,
                    'status': 'Processed',
                    'process_date': timezone.now(),
                }
            )
        
        return redirect('payroll_list')
    
    context = {
        'current_month': timezone.now().month,
        'current_year': timezone.now().year,
    }
    
    return render(request, 'payroll/process_payroll.html', context)


# ============= PAYSLIP VIEWS =============
@login_required
def payslip_list(request):
    """View all generated payslips"""
    
    payslips = Payslip.objects.select_related('employee').order_by('-generated_date')
    
    # Filter by employee if provided
    emp_id = request.GET.get('employee')
    if emp_id:
        payslips = payslips.filter(employee_id=emp_id)
    
    employees = Employee.objects.all()
    
    context = {
        'payslips': payslips,
        'employees': employees,
        'selected_employee': emp_id,
    }
    
    return render(request, 'payslips/payslip_list.html', context)


@login_required
def generate_payslip(request, payroll_id):
    """Generate payslip from payroll"""
    
    payroll = get_object_or_404(Payroll, id=payroll_id)
    
    # Check if payslip already exists
    payslip = Payslip.objects.filter(payroll=payroll).first()
    
    if not payslip:
        # Get deductions
        deduction = getattr(payroll.employee, 'deductions', None)
        
        salary_structure = payroll.employee.salary_structure
        
        # Generate payslip number
        payslip_number = f"PS-{payroll.employee_id}-{payroll.month}-{payroll.year}"
        
        payslip = Payslip.objects.create(
            payroll=payroll,
            employee=payroll.employee,
            payslip_number=payslip_number,
            basic_salary=payroll.basic_salary,
            allowances=payroll.allowances,
            gross_salary=payroll.gross_salary,
            income_tax=deduction.income_tax if deduction else 0,
            provident_fund=deduction.provident_fund if deduction else 0,
            esi=deduction.esi if deduction else 0,
            other_deductions=deduction.other_deductions if deduction else 0,
            total_deductions=payroll.total_deductions,
            net_salary=payroll.net_salary,
        )
    
    context = {
        'payslip': payslip,
        'payroll': payroll,
    }
    
    return render(request, 'payslips/payslip_detail.html', context)


@login_required
def payslip_pdf(request, payslip_id):
    """Generate PDF payslip"""
    
    payslip = get_object_or_404(Payslip, id=payslip_id)
    
    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1F2937'),
        spaceAfter=12,
        alignment=1
    )
    
    # Title
    elements.append(Paragraph("PAYSLIP", title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Company and Employee Info
    emp_info = [
        ['Company:', 'Gurunak College Payroll System'],
        ['Employee:', payslip.employee.name],
        ['Employee ID:', payslip.employee.employee_id],
        ['Position:', payslip.employee.position],
        ['Department:', payslip.employee.department.name],
    ]
    
    emp_table = Table(emp_info, colWidths=[2*inch, 4*inch])
    emp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(emp_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Salary Details
    salary_data = [
        ['Description', 'Amount (₹)'],
        ['Basic Salary', f'{payslip.basic_salary:.2f}'],
        ['Allowances', f'{payslip.allowances:.2f}'],
        ['Gross Salary', f'{payslip.gross_salary:.2f}'],
        ['', ''],
        ['Deductions', ''],
        ['Income Tax', f'{payslip.income_tax:.2f}'],
        ['Provident Fund', f'{payslip.provident_fund:.2f}'],
        ['ESI', f'{payslip.esi:.2f}'],
        ['Other Deductions', f'{payslip.other_deductions:.2f}'],
        ['Total Deductions', f'{payslip.total_deductions:.2f}'],
        ['', ''],
        ['Net Salary', f'{payslip.net_salary:.2f}'],
    ]
    
    salary_table = Table(salary_data, colWidths=[4*inch, 2*inch])
    salary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightblue),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ]))
    
    elements.append(salary_table)
    
    # Build PDF
    doc.build(elements)
    
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="payslip_{payslip.payslip_number}.pdf"'
    
    return response


# ============= REPORT VIEWS =============
@login_required
def report_list(request):
    """View all payroll reports"""
    
    reports = PayrollReport.objects.order_by('-generated_date')
    
    context = {
        'reports': reports,
    }
    
    return render(request, 'reports/report_list.html', context)


@login_required
def generate_report(request):
    """Generate payroll report"""
    
    if request.method == 'POST':
        month_from = int(request.POST.get('month_from'))
        month_to = int(request.POST.get('month_to'))
        year = int(request.POST.get('year'))
        report_type = request.POST.get('report_type')
        report_name = request.POST.get('report_name')
        
        # Get payrolls
        payrolls = Payroll.objects.filter(
            month__gte=month_from,
            month__lte=month_to,
            year=year,
            status='Approved'
        )
        
        # Calculate totals
        totals = payrolls.aggregate(
            total_employees=Count('id', distinct=True),
            total_gross=Coalesce(Sum('gross_salary', output_field=FloatField()), Value(0.0, output_field=FloatField())),
            total_deductions=Coalesce(Sum('total_deductions', output_field=FloatField()), Value(0.0, output_field=FloatField())),
            total_net=Coalesce(Sum('net_salary', output_field=FloatField()), Value(0.0, output_field=FloatField())),
        )
        
        # Create report
        report = PayrollReport.objects.create(
            name=report_name,
            report_type=report_type,
            month_from=month_from,
            month_to=month_to,
            year=year,
            total_employees=totals['total_employees'],
            total_gross_salary=totals['total_gross'],
            total_deductions=totals['total_deductions'],
            total_net_salary=totals['total_net'],
            generated_by=request.user.username,
        )
        
        return redirect('report_detail', report_id=report.id)
    
    context = {
        'current_month': timezone.now().month,
        'current_year': timezone.now().year,
    }
    
    return render(request, 'reports/generate_report.html', context)


@login_required
def report_detail(request, report_id):
    """View detailed report"""
    
    report = get_object_or_404(PayrollReport, id=report_id)
    
    # Get payrolls for this report
    payrolls = Payroll.objects.filter(
        month__gte=report.month_from,
        month__lte=report.month_to,
        year=report.year,
        status='Approved'
    ).select_related('employee')
    
    context = {
        'report': report,
        'payrolls': payrolls,
    }
    
    return render(request, 'reports/report_detail.html', context)
