from django.core.management.base import BaseCommand
from payroll.models import Department

class Command(BaseCommand):
    help = 'Create initial departments'

    def handle(self, *args, **options):
        departments = [
            {'name': 'Human Resources', 'description': 'HR and Recruitment'},
            {'name': 'Finance', 'description': 'Finance and Accounts'},
            {'name': 'Operations', 'description': 'Operations and Logistics'},
            {'name': 'Information Technology', 'description': 'IT and Software Development'},
            {'name': 'Sales', 'description': 'Sales and Marketing'},
            {'name': 'Administration', 'description': 'Administrative Support'},
        ]
        
        for dept_data in departments:
            dept, created = Department.objects.get_or_create(
                name=dept_data['name'],
                defaults={'description': dept_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created department: {dept.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Department already exists: {dept.name}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully completed initial setup'))
