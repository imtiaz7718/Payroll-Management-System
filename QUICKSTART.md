# Quick Start Guide - Payroll Management System

## ⚡ Quick Setup (5 Minutes)

### 1. Open Command Prompt/PowerShell and navigate to project directory:
```bash
cd "c:\Users\Dell\3D Objects\College projects\gurunak clg projects\payroll_project"
```

### 2. Activate Virtual Environment:
```bash
.\.venv\Scripts\activate
```

### 3. Install Dependencies:
```bash
pip install -r requirements.txt
```

### 4. Run Migrations (First Time Only):
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Admin User:
```bash
python manage.py createsuperuser
# Enter username, email, password when prompted
```

### 6. Create Sample Departments:
```bash
python manage.py create_departments
```

### 7. Start Development Server:
```bash
python manage.py runserver
```

### 8. Access the Application:
- **Main Application**: http://localhost:8000/ → Login with created credentials
- **Admin Panel**: http://localhost:8000/admin/ → Manage system

---

## 📋 Navigation Guide

### Dashboard (Home)
- Overview of system statistics
- Charts and analytics
- Quick access buttons

### Employee Management (Employees)
- **Employee List**: View all employees
- **Add Employee**: Create new employee record
- **Employee Details**: View full profile
- **Edit Employee**: Update employee information
- **Delete Employee**: Mark as inactive

### Attendance (Employees → Attendance)
- **Attendance List**: View attendance records by month
- **Mark Attendance**: Daily attendance marking
  - Present
  - Absent
  - Leave
  - Half Day

### Salary Management (Salary)
- **Salary Structure**: View and manage salary components
- **Edit Salary**: Configure allowances
- **Deductions**: Manage tax and insurance deductions

### Payroll (Salary → Payroll)
- **Payroll List**: View processed payrolls
- **Process Payroll**: Run monthly payroll calculation
  - Automatically calculates based on attendance
  - Applies deductions
  - Generates net salary

### Payslips (Payslips)
- **View Payslips**: List of all generated payslips
- **Generate Payslip**: Create from processed payroll
- **Download PDF**: Get printable version

### Reports (Reports)
- **Report List**: View all generated reports
- **Generate Report**: Create custom payroll report
- **Report Details**: Analyze report data

---

## 🔐 Default Login

Use the superuser credentials created in step 5 of Quick Start

---

## 📊 Sample Workflow

1. **Create Organization Structure**
   - Add Departments (already created via command)
   - Departments: HR, Finance, IT, Operations, Sales, Admin

2. **Add Employees**
   - Go to Employees → Add Employee
   - Fill complete information
   - System auto-generates Employee ID

3. **Configure Salary Structure**
   - Go to Salary → Salary Structure
   - Edit salary components for each employee
   - Set allowances (DA, HRA, Medical, etc.)

4. **Setup Deductions**
   - Go to Salary → Deductions
   - Configure tax and insurance deductions per employee

5. **Mark Attendance**
   - Go to Employees → Mark Attendance
   - Select date and mark for each employee
   - Mark with status: Present/Absent/Leave/Half-Day

6. **Process Payroll**
   - Go to Salary → Payroll → Process Payroll
   - Select month and year
   - System processes and calculates all salaries

7. **Generate Payslips**
   - Go to Payslips
   - Click Generate for each processed payroll
   - View or download as PDF

8. **Generate Reports**
   - Go to Reports → Generate Report
   - Select report parameters
   - View comprehensive payroll analysis

---

## 📁 Project File Structure

```
payroll_project/
├── payroll/
│   ├── models.py              # Database models
│   ├── views.py               # View functions
│   ├── urls.py                # URL patterns
│   ├── admin.py               # Admin configuration
│   ├── forms.py               # Form definitions
│   ├── migrations/            # Database migrations
│   │   └── 0001_initial.py   # Initial migration
│   └── management/
│       └── commands/
│           └── create_departments.py
├── payroll_project/
│   ├── settings.py            # Django settings
│   ├── urls.py                # Main URLs
│   └── wsgi.py
├── templates/
│   ├── base.html              # Main template
│   ├── dashboard.html         # Home page
│   ├── login.html
│   ├── employees/             # Employee templates
│   ├── attendance/            # Attendance templates
│   ├── salary/                # Salary templates
│   ├── deductions/            # Deduction templates
│   ├── payroll/               # Payroll templates
│   ├── payslips/              # Payslip templates
│   └── reports/               # Report templates
├── db.sqlite3                 # Database file
├── manage.py                  # Management script
├── requirements.txt           # Dependencies
└── README.md                  # Documentation
```

---

## 🎨 UI Features

### Modern Design Elements
- **Gradient Backgrounds**: Purple to blue gradients
- **Glass Morphism**: Semi-transparent cards with blur
- **Smooth Animations**: Slide-in and fade-up effects
- **Responsive Layout**: Mobile-friendly design
- **Interactive Charts**: Real-time data visualization
- **Color-Coded Badges**: Status indicators

### Navigation
- **Top Navbar**: Quick access to all modules
- **Dropdown Menus**: Organized section access
- **Breadcrumb**: Current page indication
- **Quick Actions**: Fast task buttons

---

## 💾 Database Details

### SQLite Database
- File: `db.sqlite3`
- Auto-created on first migrate
- Contains all employee, payroll, and transaction data

### Tables Created
1. `Employee` - Employee records
2. `Department` - Organization departments
3. `Attendance` - Daily attendance
4. `SalaryStructure` - Salary components
5. `Deduction` - Tax and insurance deductions
6. `Payroll` - Monthly payroll calculations
7. `Payslip` - Generated payslips
8. `PayrollReport` - Generated reports

---

## ⚙️ Configuration

### Django Settings (settings.py)
- DEBUG = True (for development)
- ALLOWED_HOSTS = [] (configure for production)
- DATABASE = SQLite (can switch to MySQL)

### Email Configuration (Optional)
Add to settings.py for email features:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

---

## 🐛 Troubleshooting

### Issue: Python command not found
**Solution**: Activate virtual environment
```bash
.\.venv\Scripts\activate
```

### Issue: Django module not found
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Port 8000 already in use
**Solution**: Use different port
```bash
python manage.py runserver 8080
# Access at http://localhost:8080/
```

### Issue: Database locked error
**Solution**: Delete db.sqlite3 and recreate
```bash
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Issue: No departments available
**Solution**: Run setup command
```bash
python manage.py create_departments
```

---

## 🚀 Deployment Tips

### For Production:
1. Set DEBUG = False in settings.py
2. Set ALLOWED_HOSTS with your domain
3. Use MySQL instead of SQLite
4. Set up proper email configuration
5. Use environment variables for secrets
6. Deploy on AWS EC2, Heroku, or DigitalOcean

### Database Migration to MySQL:
1. Install: `pip install mysql-connector-python`
2. Update DATABASES in settings.py
3. Run: `python manage.py migrate`

---

## 📊 Performance Tips

1. **Add Database Indexes**
   - Already configured for Employee ID and Status

2. **Use Caching**
   - Cache department list
   - Cache employee summaries

3. **Optimize Queries**
   - Use select_related() for ForeignKey
   - Use prefetch_related() for reverse relations

4. **Pagination**
   - Implement on employee list
   - Implement on report pages

---

## 🔒 Security Checklist

- [x] User authentication required
- [x] CSRF token on all forms
- [x] SQL injection prevention via ORM
- [x] Password hashing
- [x] Input validation
- [ ] HTTPS (configure for production)
- [ ] Rate limiting
- [ ] API key management

---

## 📞 Support

For issues or questions:
1. Check README.md
2. Review logs in console
3. Check Django admin panel for data
4. Verify database migrations: `python manage.py showmigrations`

---

**Enjoy using the Payroll Management System! 🎉**

Last Updated: February 21, 2026
