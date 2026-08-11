# SETUP GUIDE - Payroll Management System

## 📋 Pre-requisites
- Python 3.8 or higher
- pip (Python Package Manager)
- Git (optional)
- Terminal or Command Prompt

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Navigate to Project Directory
```bash
cd c:\Users\Dell\3D Objects\College projects\gurunak clg projects\payroll_project
```

### Step 2: Create Virtual Environment
```bash
# Windows (PowerShell or CMD)
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\activate

# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
# Upgrade pip first
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

### Step 4: Apply Database Migrations
```bash
python manage.py migrate
```

### Step 5: Create Superuser Account
```bash
python manage.py createsuperuser
```
Enter the following when prompted:
- **Username**: admin
- **Email**: admin@company.com
- **Password**: (choose a secure password, e.g., Admin@123)

### Step 6: Populate Sample Data (Optional)
```bash
python populate_sample_data.py
```
This adds:
- 5 departments
- 5 sample employees
- Salary structures for each employee
- Deductions for each employee
- 30 days of sample attendance records

### Step 7: Start Development Server
```bash
python manage.py runserver
```

The server will start on: **http://localhost:8000/**

---

## 🔐 Accessing the System

### Login Page
- **URL**: http://localhost:8000/login/
- **Username**: admin (or your created superuser)
- **Password**: Your chosen password

### Admin Panel
- **URL**: http://localhost:8000/admin/
- Access all models, add/edit/delete records manually
- Manage system configuration

### Dashboard
- **URL**: http://localhost:8000/ (after login)
- View statistics, charts, and recent activities
- Access all modules from navigation menu

---

## 📚 System Modules

### 1. **Employee Management** (`/employees/`)
- View all employees
- Add new employee
- Edit employee information
- Delete (deactivate) employee
- View employee details and salary structure

### 2. **Attendance Tracking** (`/attendance/`)
- View attendance records
- Mark attendance for employees
- Filter by month/year
- View attendance statistics

### 3. **Salary Structure** (`/salary-structure/`)
- Configure salary components
- View gross salary calculation
- Edit allowances for employees

### 4. **Deductions Management** (`/deductions/`)
- Manage tax deductions
- Configure insurance deductions
- Apply loan adjustments

### 5. **Payroll Processing** (`/payroll/`)
- Process monthly payroll
- Automatic calculation based on attendance
- Multiple workflow statuses

### 6. **Payslip Generation** (`/payslips/`)
- Generate payslips for employees
- Download payslips as PDF
- View detailed breakdowns

### 7. **Reports** (`/reports/`)
- Generate payroll reports
- View payroll analytics
- Date-range filtering

---

## 🎯 Sample Workflow

### 1. Login to System
```
URL: http://localhost:8000/login/
Username: admin
Password: [Your password]
```

### 2. Create an Employee (if not using sample data)
```
1. Go to Employees → Add Employee
2. Fill in all required fields
3. Configure salary components
4. Configure deductions
5. Click Submit
```

### 3. Mark Attendance
```
1. Go to Attendance → Mark Attendance
2. Select current date
3. Select status for each employee (Present/Absent/Leave)
4. Add remarks (optional)
5. Click Submit
```

### 4. Process Monthly Payroll
```
1. Go to Payroll → Process Payroll
2. Select month and year
3. Review calculated gross salary
4. Click Process Payroll
5. System automatically calculates based on attendance
```

### 5. Generate Payslips
```
1. Go to Payslips
2. Click Generate for desired payroll
3. Review payslip details
4. Download as PDF
```

### 6. Generate Reports
```
1. Go to Reports → Generate Report
2. Select report type and date range
3. Click Generate
4. View comprehensive payroll analytics
```

---

## 🔧 Configuration

### Database (settings.py)
Current: **SQLite3** (development)

To use **MySQL** in production:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'payroll_db',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Email Configuration
Add to `settings.py` for email notifications:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Static Files Collection
For production:
```bash
python manage.py collectstatic
```

---

## 🐛 Troubleshooting

### Virtual Environment Issues
```bash
# If activation fails, try:
# Windows CMD:
.venv\Scripts\activate.bat

# Windows PowerShell (if execution policy error):
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Django Migration Errors
```bash
# Reset migrations (⚠️ Clears database):
python manage.py migrate payroll zero

# Recreate migrations:
python manage.py makemigrations
python manage.py migrate
```

### Port Already in Use
```bash
# Use different port:
python manage.py runserver 8001
```

### Module Import Errors
```bash
# Verify Python path:
python -c "import sys; print(sys.executable)"

# Reinstall packages:
pip install --force-reinstall -r requirements.txt
```

### Database Locked Error
```bash
# Remove old database:
del db.sqlite3

# Recreate database:
python manage.py migrate
python manage.py createsuperuser
```

---

## 📁 Project Structure

```
payroll_project/
├── manage.py                 # Django management script
├── db.sqlite3               # SQLite database
├── requirements.txt         # Python dependencies
├── sample_data.json         # Sample data template
├── populate_sample_data.py  # Script to populate data
│
├── payroll_project/         # Main Django project settings
│   ├── settings.py         # Project configuration
│   ├── urls.py             # Main URL routing
│   ├── asgi.py
│   └── wsgi.py
│
├── payroll/                 # Main application
│   ├── models.py           # 8 data models
│   ├── views.py            # 20+ view functions
│   ├── urls.py             # App URL patterns
│   ├── forms.py            # 5 form classes
│   ├── admin.py            # Admin configuration
│   ├── migrations/         # Database migrations
│   └── tests.py
│
└── templates/              # 30+ HTML templates
    ├── base.html           # Master template
    ├── login.html          # Login page
    ├── dashboard.html      # Dashboard
    ├── employees/          # Employee templates
    ├── attendance/         # Attendance templates
    ├── salary/             # Salary templates
    ├── deductions/         # Deduction templates
    ├── payroll/            # Payroll templates
    ├── payslips/           # Payslip templates
    └── reports/            # Report templates
```

---

## 🌐 URLs Cheat Sheet

| Feature | URL |
|---------|-----|
| Dashboard | `/` |
| Login | `/login/` |
| Admin Panel | `/admin/` |
| Employees | `/employees/` |
| Add Employee | `/employees/add/` |
| Attendance | `/attendance/` |
| Mark Attendance | `/attendance/mark/` |
| Salary Structure | `/salary-structure/` |
| Deductions | `/deductions/` |
| Payroll | `/payroll/` |
| Process Payroll | `/payroll/process/` |
| Payslips | `/payslips/` |
| Reports | `/reports/` |
| Generate Report | `/reports/generate/` |

---

## 🎨 UI Features

### Design Elements
- **Glass Morphism**: Frosted glass card effects with blur
- **Gradients**: Modern gradient backgrounds
- **Animations**: Smooth transitions and keyframe animations
- **Responsive**: Mobile-friendly Bootstrap layout
- **Icons**: Font Awesome icons throughout

### Charts & Visualizations
- Position distribution bar chart
- Attendance status doughnut chart
- Real-time salary calculations
- Interactive data tables with filtering

---

## 🔒 Security Features

### Built-in Security
- CSRF token protection
- SQL injection prevention (via Django ORM)
- XSS protection
- Password hashing
- Session management
- Login required decorators

### Best Practices
- Use strong passwords
- Keep SECRET_KEY secure
- Use HTTPS in production
- Regular database backups
- Update Django version regularly

---

## 📊 Sample Data Details

### Departments
- Human Resources
- Finance
- Information Technology
- Operations
- Sales

### Employees (5 sample)
1. **Rajesh Kumar** - Manager (HR) - ₹75,000
2. **Priya Singh** - Senior Developer (IT) - ₹85,000
3. **Amit Patel** - Junior Developer (IT) - ₹45,000
4. **Neha Sharma** - Accountant (Finance) - ₹55,000
5. **Vikas Gupta** - Sales Executive (Sales) - ₹50,000

---

## 💡 Tips & Tricks

### Bulk Employee Import
Use admin panel to import via CSV (requires django-import-export)

### Automated Payroll Processing
Create a cron job or celery task to auto-process monthly payroll

### Email Notifications
Configure email backend to send payslips automatically

### PDF Customization
Modify `payslip_pdf()` view to match company branding

### Data Export
Use Django's admin export functionality or create custom reports

---

## 🚀 Deployment

### Using Heroku
```bash
pip install gunicorn
echo web: gunicorn payroll_project.wsgi > Procfile
git push heroku main
```

### Using AWS/DigitalOcean
```bash
# Install gunicorn and nginx
pip install gunicorn
# Configure nginx as reverse proxy
# Run: gunicorn payroll_project.wsgi:application
```

### Using Docker
```dockerfile
FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["gunicorn", "payroll_project.wsgi"]
```

---

## 📞 Support & Help

### Common Issues
1. **ImportError**: Check virtual environment activation
2. **Database errors**: Run migrations
3. **Static files**: Run collectstatic
4. **Permission denied**: Check file permissions

### Documentation
- Django Official: https://docs.djangoproject.com/
- Bootstrap: https://getbootstrap.com/
- Chart.js: https://www.chartjs.org/

---

## 🎓 Learning Path

1. **Week 1**: Understand Django MVT architecture
2. **Week 2**: Learn ORM and model relationships
3. **Week 3**: Master views and URL routing
4. **Week 4**: Customize templates and styling
5. **Week 5**: Deploy to production

---

## 📝 Maintenance

### Regular Tasks
- Backup database weekly
- Update dependencies monthly
- Monitor server logs
- Clean old payroll records (archive)

### Performance Optimization
- Use database indexes (already configured)
- Implement caching for reports
- Optimize queries with select_related
- Minify CSS/JavaScript

---

## ✅ Checklist - First Time Setup

- [ ] Python installed and verified
- [ ] Virtual environment created and activated
- [ ] Dependencies installed from requirements.txt
- [ ] Database migrated
- [ ] Superuser created
- [ ] Sample data populated (optional)
- [ ] Server started successfully
- [ ] Login working with superuser
- [ ] Dashboard accessible
- [ ] Admin panel functional

---

**Happy payroll processing! 🎉**

For detailed documentation, see [README.md](README.md) and [QUICKSTART.md](QUICKSTART.md)
