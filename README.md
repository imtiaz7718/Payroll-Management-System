# Payroll Management System

Project Link: https://payroll-management-system-3-5h6q.onrender.com/login/?next=/
username: admin
password: AdminPass123!

## Complete HR & Payroll Automation Platform

### Project Overview
A comprehensive enterprise-level Payroll Management System built with Django and MySQL that automates employee salary processing, attendance tracking, and payroll operations. The system ensures accuracy in payroll calculations, reduces manual errors, and maintains complete compliance with statutory regulations.

---

## 🎯 System Features

### 1. **Employee Management Module**
- ✅ Complete employee profile management
- ✅ Multiple positions and departments
- ✅ Employee ID generation (automatic)
- ✅ Contact details and address management
- ✅ Tax information (PAN, Aadhar)
- ✅ Bank details for salary transfer
- ✅ Employment status tracking (Active/Inactive/On Leave)
- ✅ Advanced search and filtering
- ✅ Quick employee directory

### 2. **Attendance Management Module**
- ✅ Daily attendance marking
- ✅ Attendance status (Present/Absent/Leave/Half-Day)
- ✅ Monthly attendance reports
- ✅ Attendance statistics and analytics
- ✅ Remarks for special attendance cases

### 3. **Salary Structure Module**
- ✅ Base salary management
- ✅ Allowances configuration
  - Dearness Allowance (DA)
  - House Rent Allowance (HRA)
  - Medical Allowance
  - Conveyance Allowance
  - Other custom allowances
- ✅ Gross salary calculation
- ✅ Real-time gross salary display

### 4. **Deduction Management Module**
- ✅ Multiple deduction types:
  - Income Tax (IT)
  - Provident Fund (PF)
  - Employee State Insurance (ESI)
  - Health Insurance
  - Professional Tax
  - Loan deductions
  - Custom deductions
- ✅ Total deduction calculation
- ✅ Centralized deduction management

### 5. **Payroll Processing Module**
- ✅ Automated monthly payroll processing
- ✅ Attendance-based salary calculation
- ✅ Automatic deduction application
- ✅ Attendance-based salary adjustment (pro-rata)
- ✅ Status tracking (Draft/Processed/Approved)
- ✅ Payroll summary and totals
- ✅ Batch payroll processing

### 6. **Payslip Generation Module**
- ✅ Detailed payslips generation
- ✅ Professional payslip format
- ✅ Component-wise breakdown
  - Earnings summary
  - Deductions summary
  - Net salary calculation
- ✅ PDF download functionality
- ✅ Email-ready payslips
- ✅ Unique payslip numbering

### 7. **Report Management Module**
- ✅ Monthly payroll reports
- ✅ Quarterly salary summaries
- ✅ Annual payroll reports
- ✅ Custom date range reports
- ✅ Department-wise salary reports
- ✅ Employee-wise payroll history
- ✅ Total payroll summaries
- ✅ Compliance reports

---

## 📊 Dashboard Features

### Overview Statistics
- Total active employees
- Present/Absent today count
- Employees on leave
- Total monthly payroll

### Visual Analytics
- **Position Distribution Chart** - Employee breakdown by position
- **Attendance Status Chart** - Present, Absent, Leave statistics
- **Recent Payroll Summary** - Latest payroll transactions
- **Recent Payslips** - Recently generated payslips

### Quick Actions
- Add new employee
- Mark daily attendance
- Process monthly payroll
- Generate reports

---

## 🛠 Technology Stack

### Backend
- **Framework**: Django 4.2
- **Language**: Python 3.12
- **Database**: SQLite (Can be migrated to MySQL)

### Frontend
- **HTML5**, **CSS3**, **JavaScript**
- **Bootstrap 5.3** - Responsive design
- **Chart.js 4** - Data visualization
- **Font Awesome 6.5** - Icons

### Additional Libraries
- **ReportLab** - PDF generation
- **Django ORM** - Database abstraction

---

## 🎨 UI/UX Features

### Modern Design
- Glass Morphism UI
- Gradient backgrounds
- Smooth animations
- Responsive layout
- Dark-themed interface
- Beautiful color themes

### Interactive Elements
- Animated cards
- Hover effects
- Loading spinners
- Toast notifications
- Modal dialogs
- Filter dropdowns

### Charts & Graphs
- Bar charts for position distribution
- Pie charts for attendance status
- Real-time statistics
- Color-coded status badges

---

## 📋 Database Models

### 1. **Department**
- Department name
- Description
- Creation timestamps

### 2. **Employee**
- Personal information (Name, Email, Phone)
- Employment details (ID, Position, Department, Experience)
- Address and contact details
- Tax information (PAN, Aadhar)
- Bank details (Account, IFSC)
- Employment status
- Timestamps

### 3. **Attendance**
- Employee reference
- Date
- Status (Present/Absent/Leave/Half-Day)
- Remarks
- Timestamps

### 4. **SalaryStructure**
- Employee reference (One-to-One)
- Base salary
- Various allowances configuration
- Calculated gross salary
- Timestamps

### 5. **Deduction**
- Employee reference (One-to-One)
- Deduction types and amounts
- Calculated total deductions
- Timestamps

### 6. **Payroll**
- Employee reference
- Month and year
- Days worked / total days
- Gross salary calculations
- Deductions total
- Net salary
- Status (Draft/Processed/Approved/Rejected)
- Timestamps

### 7. **Payslip**
- Payroll reference (One-to-One)
- Employee reference
- Payslip unique number
- Earnings details
- Deductions details
- Net salary
- Generated date

### 8. **PayrollReport**
- Report name and type
- Month range
- Employee count
- Total salary calculations
- Generated by user
- Generation timestamp

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.12
- pip (Python package manager)
- Virtual Environment (recommended)

### Step 1: Clone Repository
```bash
cd "c:\Users\Dell\3D Objects\College projects\gurunak clg projects\payroll_project"
```

### Step 2: Create Virtual Environment
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install django reportlab
```

### Step 4: Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 6: Create Initial Departments
```bash
python manage.py create_departments
```

### Step 7: Run Development Server
```bash
python manage.py runserver
```

### Step 8: Access the Application
- Main Application: http://localhost:8000/
- Admin Panel: http://localhost:8000/admin/
- Login required for all features

---

## 📱 System Workflow

```
┌─────────────────────────────────────────────────┐
│  Admin Interface - Login & Dashboard            │
├─────────────────────────────────────────────────┤
│  Employee Management                            │
│  ↓                                              │
│  Attendance Recording                           │
│  ↓                                              │
│  Salary Structure & Deductions Configuration    │
│  ↓                                              │
│  Payroll Processing (Monthly/Quarterly)         │
│  ↓                                              │
│  Payslip Generation & PDF Export                │
│  ↓                                              │
│  Report Generation & Analysis                   │
├─────────────────────────────────────────────────┤
│  Database (SQLite/MySQL)                        │
└─────────────────────────────────────────────────┘
```

---

## 🔐 Security Features

- Django's built-in authentication system
- Login-required decorators on all views
- CSRF token protection on forms
- SQL injection prevention via ORM
- Admin interface role-based access
- Data validation on all inputs
- Secure password handling

---

## 📊 Sample Data Structure

### Employee Example:
- Name: John Doe
- Employee ID: EMP1001
- Position: Manager
- Department: Finance
- Base Salary: ₹50,000
- Allowances: DA (₹5,000) + HRA (₹10,000) = ₹15,000
- Gross Salary: ₹65,000
- Deductions: IT (₹10,000) + PF (₹6,500) = ₹16,500
- Net Salary: ₹48,500

---

## 📈 Payroll Calculation Formula

```
┌─────────────────────────────────────┐
│ Gross Salary Calculation            │
├─────────────────────────────────────┤
│ Base Salary                         │
│ + Dearness Allowance (DA)           │
│ + House Rent Allowance (HRA)        │
│ + Medical Allowance                 │
│ + Conveyance Allowance              │
│ + Other Allowances                  │
│ = GROSS SALARY                      │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│ Deductions                          │
├─────────────────────────────────────┤
│ - Income Tax (IT)                   │
│ - Provident Fund (PF)               │
│ - Employee State Insurance (ESI)    │
│ - Health Insurance                  │
│ - Professional Tax                  │
│ - Loan Deductions                   │
│ = TOTAL DEDUCTIONS                  │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│ NET SALARY = Gross - Deductions     │
│ (Payable Amount)                    │
└─────────────────────────────────────┘
```

---

## 📝 Project Structure

```
payroll_project/
├── payroll/
│   ├── models.py                 # Database models
│   ├── views.py                  # Business logic & views
│   ├── urls.py                   # URL routing
│   ├── admin.py                  # Django admin configuration
│   ├── forms.py                  # Django forms
│   ├── migrations/               # Database migrations
│   └── management/
│       └── commands/
│           └── create_departments.py
├── payroll_project/
│   ├── settings.py               # Project settings
│   ├── urls.py                   # Main URL configuration
│   └── wsgi.py                   # WSGI configuration
├── templates/
│   ├── base.html                 # Main template
│   ├── dashboard.html            # Dashboard template
│   ├── login.html                # Login template
│   ├── employees/                # Employee templates
│   ├── attendance/               # Attendance templates
│   ├── salary/                   # Salary structure templates
│   ├── deductions/               # Deductions templates
│   ├── payroll/                  # Payroll templates
│   ├── payslips/                 # Payslip templates
│   └── reports/                  # Report templates
├── manage.py                     # Django management script
├── db.sqlite3                    # SQLite database
└── README.md                     # This file
```

---

## 🎓 Key Concepts Demonstrated

1. **Object-Oriented Design (OOP)**
   - Model-View-Template architecture
   - Class-based organization

2. **Database Design**
   - Normalized database schema
   - Relationships (ForeignKey, OneToOneField)
   - Indexes for performance

3. **Business Logic**
   - Complex payroll calculations
   - Attendance-based salary adjustments
   - Automated deduction processing

4. **Security**
   - User authentication
   - Authorization checks
   - Data validation

5. **UI/UX Design**
   - Responsive web design
   - Modern aesthetics
   - Interactive components

6. **Data Visualization**
   - Charts and graphs
   - Statistics dashboard
   - Report generation

---

## 📞 Support & Maintenance

### Common Issues

**Django Not Found?**
- Ensure virtual environment is activated
- Run: `pip install django reportlab`

**Database Errors?**
- Delete `db.sqlite3` and migrations (except `__init__.py`)
- Run: `python manage.py makemigrations`
- Run: `python manage.py migrate`

**PDF Generation Issues?**
- Ensure ReportLab is installed
- Run: `pip install reportlab`

---

## 🔄 Future Enhancements

- [ ] Email integration for payslip distribution
- [ ] Excel export for reports
- [ ] Mobile app (React Native)
- [ ] Salary advance system
- [ ] Leave management integration
- [ ] Performance evaluation module
- [ ] API for third-party integration
- [ ] Multi-language support
- [ ] Cloud deployment (AWS, Heroku)
- [ ] Analytics dashboard with ML predictions

---

## 📄 License

This project is for educational purposes. Feel free to use and modify as needed.

---

## ✨ Acknowledgments

Built for Gurunak College as a comprehensive HR management system demonstrating real-world Django application development, database design, and enterprise software architecture.

**Developed by:** GitHub Copilot with Claude Haiku 4.5
**Year:** 2026
**Version:** 1.0

---

## 📞 Contact & Support

For issues, suggestions, or improvements, please reach out through the project documentation or administrative contact.

---

**Happy Payroll Processing! 🎉**

This project is done during Feb 2026
