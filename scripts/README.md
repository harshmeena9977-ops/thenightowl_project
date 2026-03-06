# Django Scripts & Commands Documentation

## Management Scripts Overview

This section contains essential Django management commands and utility scripts for the NightOwl project.

## Database Management Scripts

### Database Setup Script
```python
# scripts/setup_database.py
import os
import django
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def setup_database():
    """Initialize database with basic data"""
    from django.contrib.auth.models import User
    from nightowlmainapp.models import UserProfile, Project
    
    # Create admin user
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@nightowl.com',
            password='admin123'
        )
        UserProfile.objects.create(user=admin, role='designer')
        print("Admin user created successfully")
    
    # Create sample designer
    if not User.objects.filter(username='designer1').exists():
        designer = User.objects.create_user(
            username='designer1',
            email='designer1@nightowl.com',
            password='designer123'
        )
        UserProfile.objects.create(user=designer, role='designer')
        print("Sample designer created successfully")
    
    # Create sample client
    if not User.objects.filter(username='client1').exists():
        client = User.objects.create_user(
            username='client1',
            email='client1@nightowl.com',
            password='client123'
        )
        UserProfile.objects.create(user=client, role='client')
        print("Sample client created successfully")

if __name__ == '__main__':
    setup_database()
```

### Data Migration Script
```python
# scripts/migrate_data.py
import os
import django
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def migrate_sample_data():
    """Migrate sample data for development"""
    from nightowlmainapp.models import Project
    from django.contrib.auth.models import User
    
    # Get sample designer
    designer = User.objects.get(username='designer1')
    
    # Create sample projects
    sample_projects = [
        {
            'title': 'E-commerce Website Redesign',
            'description': 'Complete redesign of e-commerce platform with modern UI/UX',
            'client': 'TechCorp Solutions'
        },
        {
            'title': 'Mobile App Development',
            'description': 'Native iOS and Android app for food delivery service',
            'client': 'FoodieExpress'
        },
        {
            'title': 'Brand Identity Design',
            'description': 'Complete brand identity including logo, colors, and guidelines',
            'client': 'StartupHub'
        }
    ]
    
    for project_data in sample_projects:
        if not Project.objects.filter(title=project_data['title']).exists():
            Project.objects.create(
                title=project_data['title'],
                description=project_data['description'],
                client=project_data['client'],
                designer=designer
            )
            print(f"Created project: {project_data['title']}")

if __name__ == '__main__':
    migrate_sample_data()
```

## User Management Scripts

### User Creation Script
```python
# scripts/create_users.py
import os
import django
from django.contrib.auth.models import User
from nightowlmainapp.models import UserProfile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def create_user(username, email, password, role):
    """Create user with specified role"""
    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        UserProfile.objects.create(user=user, role=role)
        print(f"Created {role} user: {username}")
        return user
    except Exception as e:
        print(f"Error creating user {username}: {e}")
        return None

def create_sample_users():
    """Create sample users for testing"""
    users = [
        ('john_designer', 'john@nightowl.com', 'designer123', 'designer'),
        ('sarah_contractor', 'sarah@nightowl.com', 'contractor123', 'contractor'),
        ('mike_client', 'mike@nightowl.com', 'client123', 'client'),
        ('lisa_designer', 'lisa@nightowl.com', 'designer123', 'designer'),
        ('tom_contractor', 'tom@nightowl.com', 'contractor123', 'contractor'),
    ]
    
    for username, email, password, role in users:
        create_user(username, email, password, role)

if __name__ == '__main__':
    create_sample_users()
```

### User Role Management Script
```python
# scripts/manage_roles.py
import os
import django
from django.contrib.auth.models import User
from nightowlmainapp.models import UserProfile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def list_users_by_role():
    """List all users grouped by role"""
    roles = UserProfile.ROLE_CHOICES
    
    for role_code, role_name in roles:
        users = UserProfile.objects.filter(role=role_code)
        print(f"\n{role_name.title()}s ({users.count()}):")
        for profile in users:
            print(f"  - {profile.user.username} ({profile.user.email})")

def change_user_role(username, new_role):
    """Change user role"""
    try:
        user = User.objects.get(username=username)
        profile = user.userprofile
        old_role = profile.role
        profile.role = new_role
        profile.save()
        print(f"Changed {username} role from {old_role} to {new_role}")
        return True
    except User.DoesNotExist:
        print(f"User {username} not found")
        return False

def delete_user(username):
    """Delete user and associated profile"""
    try:
        user = User.objects.get(username=username)
        user.delete()
        print(f"Deleted user: {username}")
        return True
    except User.DoesNotExist:
        print(f"User {username} not found")
        return False

if __name__ == '__main__':
    list_users_by_role()
```

## Project Management Scripts

### Project Creation Script
```python
# scripts/create_projects.py
import os
import django
from django.contrib.auth.models import User
from nightowlmainapp.models import Project

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def create_project(title, description, client, designer_username):
    """Create a new project"""
    try:
        designer = User.objects.get(username=designer_username)
        
        project = Project.objects.create(
            title=title,
            description=description,
            client=client,
            designer=designer
        )
        
        print(f"Created project: {title} for {client} by {designer_username}")
        return project
    except User.DoesNotExist:
        print(f"Designer {designer_username} not found")
        return None

def create_sample_projects():
    """Create sample projects for testing"""
    projects = [
        {
            'title': 'Corporate Website Development',
            'description': 'Full-stack corporate website with CMS integration',
            'client': 'GlobalTech Inc.',
            'designer_username': 'john_designer'
        },
        {
            'title': 'Logo Design Package',
            'description': 'Complete logo design with brand guidelines',
            'client': 'Local Bakery Co.',
            'designer_username': 'lisa_designer'
        },
        {
            'title': 'Web Application Development',
            'description': 'Custom web application for inventory management',
            'client': 'Retail Solutions Ltd.',
            'designer_username': 'sarah_contractor'
        }
    ]
    
    for project_data in projects:
        create_project(**project_data)

def list_projects():
    """List all projects with details"""
    projects = Project.objects.all().order_by('-created_at')
    
    print(f"\nAll Projects ({projects.count()}):")
    print("-" * 80)
    
    for project in projects:
        print(f"Title: {project.title}")
        print(f"Client: {project.client}")
        print(f"Designer: {project.designer.username}")
        print(f"Created: {project.created_at.strftime('%Y-%m-%d')}")
        print(f"Description: {project.description[:100]}...")
        print("-" * 80)

if __name__ == '__main__':
    create_sample_projects()
    list_projects()
```

## Backup and Maintenance Scripts

### Database Backup Script
```bash
#!/bin/bash
# scripts/backup_database.sh

# Configuration
DB_NAME="nightowl_db"
DB_USER="nightowl_user"
BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/nightowl_backup_$DATE.sql"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Perform backup
echo "Starting database backup..."
pg_dump -U $DB_USER -h localhost $DB_NAME > $BACKUP_FILE

if [ $? -eq 0 ]; then
    echo "Backup completed successfully: $BACKUP_FILE"
    
    # Keep only last 7 backups
    find $BACKUP_DIR -name "nightowl_backup_*.sql" -type f -mtime +7 -delete
    echo "Old backups cleaned up"
else
    echo "Backup failed"
    exit 1
fi
```

### Database Restore Script
```bash
#!/bin/bash
# scripts/restore_database.sh

if [ $# -eq 0 ]; then
    echo "Usage: $0 <backup_file.sql>"
    exit 1
fi

BACKUP_FILE=$1
DB_NAME="nightowl_db"
DB_USER="nightowl_user"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "Restoring database from: $BACKUP_FILE"
psql -U $DB_USER -h localhost -d $DB_NAME < $BACKUP_FILE

if [ $? -eq 0 ]; then
    echo "Database restored successfully"
else
    echo "Database restore failed"
    exit 1
fi
```

## Development Utility Scripts

### Development Server Script
```bash
#!/bin/bash
# scripts/dev_server.sh

echo "Starting NightOwl development server..."

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Warning: Virtual environment not activated"
    echo "Please activate virtual environment first:"
    echo "source venv/bin/activate"
    exit 1
fi

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start development server
echo "Starting development server on http://127.0.0.1:8000"
python manage.py runserver 0.0.0.0:8000
```

### Test Runner Script
```bash
#!/bin/bash
# scripts/run_tests.sh

echo "Running NightOwl test suite..."

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Warning: Virtual environment not activated"
    exit 1
fi

# Run tests with coverage
echo "Running tests with coverage..."
coverage run --source='.' manage.py test

# Generate coverage report
echo "Generating coverage report..."
coverage report

# Generate HTML coverage report
coverage html

echo "Test results:"
coverage report | tail -n 1

echo "HTML coverage report generated in htmlcov/"
```

### Code Quality Script
```bash
#!/bin/bash
# scripts/code_quality.sh

echo "Running code quality checks..."

# Check code style with flake8
echo "Checking code style with flake8..."
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Run security checks
echo "Running security checks with bandit..."
bandit -r . -f json -o bandit-report.json

# Check for common security issues
echo "Checking for common security issues..."
python manage.py check --deploy

echo "Code quality checks completed"
```

## Deployment Scripts

### Production Setup Script
```bash
#!/bin/bash
# scripts/setup_production.sh

echo "Setting up NightOwl for production..."

# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib

# Create system user
sudo useradd -m -s /bin/bash nightowl

# Setup application directory
sudo mkdir -p /opt/nightowl
sudo chown nightowl:nightowl /opt/nightowl

# Setup virtual environment
cd /opt/nightowl
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup PostgreSQL database
sudo -u postgres createdb nightowl_db
sudo -u postgres createuser --interactive nightowl_user

# Setup environment variables
echo "DJANGO_SETTINGS_MODULE=config.settings" >> .env
echo "SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" >> .env

# Collect static files
python manage.py collectstatic --noinput

# Setup systemd service
sudo cp scripts/nightowl.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable nightowl
sudo systemctl start nightowl

echo "Production setup completed"
```

### Deployment Script
```bash
#!/bin/bash
# scripts/deploy.sh

echo "Deploying NightOwl application..."

# Pull latest code
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart application
sudo systemctl restart nightowl

# Check status
sudo systemctl status nightowl

echo "Deployment completed"
```

## Usage Instructions

### Running Scripts
```bash
# Make scripts executable
chmod +x scripts/*.sh

# Run database setup
python scripts/setup_database.py

# Create sample users
python scripts/create_users.py

# Create sample projects
python scripts/create_projects.py

# Start development server
./scripts/dev_server.sh

# Run tests
./scripts/run_tests.sh

# Backup database
./scripts/backup_database.sh

# Deploy to production
./scripts/deploy.sh
```

### Custom Scripts
```python
# scripts/custom_script.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Your custom logic here
from nightowlmainapp.models import Project, UserProfile

def custom_function():
    """Your custom function"""
    projects = Project.objects.all()
    print(f"Total projects: {projects.count()}")
    
    for project in projects:
        print(f"- {project.title} (Client: {project.client})")

if __name__ == '__main__':
    custom_function()
```

## Troubleshooting

### Common Issues
1. **Module Import Errors:** Ensure Django settings are configured
2. **Database Connection:** Check database configuration and credentials
3. **Permission Errors:** Verify file permissions and user access
4. **Virtual Environment:** Ensure virtual environment is activated

### Debug Scripts
```python
# scripts/debug.py
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
    print("Django setup successful")
    
    # Test database connection
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT 1")
    print("Database connection successful")
    
    # Test model imports
    from nightowlmainapp.models import Project, UserProfile
    print("Model imports successful")
    
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
```

## Automation

### Cron Jobs
```bash
# Backup database daily at 2 AM
0 2 * * * /opt/nightowl/scripts/backup_database.sh

# Run tests weekly on Sunday at 3 AM
0 3 * * 0 /opt/nightowl/scripts/run_tests.sh

# Check application health every hour
0 * * * * /opt/nightowl/scripts/health_check.sh
```

### Health Check Script
```python
# scripts/health_check.py
import os
import sys
import django
import requests
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def check_database():
    """Check database connectivity"""
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        return True
    except:
        return False

def check_models():
    """Check model integrity"""
    try:
        from nightowlmainapp.models import Project, UserProfile
        Project.objects.count()
        UserProfile.objects.count()
        return True
    except:
        return False

def check_application():
    """Check application health"""
    try:
        response = requests.get('http://localhost:8000/', timeout=10)
        return response.status_code == 200
    except:
        return False

def main():
    checks = {
        'database': check_database(),
        'models': check_models(),
        'application': check_application()
    }
    
    all_healthy = all(checks.values())
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = "HEALTHY" if all_healthy else "UNHEALTHY"
    
    print(f"[{timestamp}] Application Status: {status}")
    
    for check_name, result in checks.items():
        status_icon = "✓" if result else "✗"
        print(f"  {status_icon} {check_name.title()}: {'OK' if result else 'FAILED'}")
    
    sys.exit(0 if all_healthy else 1)

if __name__ == '__main__':
    main()
```
