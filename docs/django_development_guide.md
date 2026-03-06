# Django Development Guide

## Application Architecture

### Project Structure Overview
```
thenightowl_project/
├── manage.py                    # Django management script
├── config/                      # Project configuration
│   ├── __init__.py
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Root URL configuration
│   └── wsgi.py                  # WSGI configuration
├── nightowlmainapp/            # Main application
├── pages/                      # Static pages app
├── accounts/                   # User management app
├── portfolio/                  # Portfolio management app
├── chat/                       # Communication features
├── payments/                   # Payment processing
└── wallets/                    # Digital wallet system
```

### Django MVT Architecture
- **Model:** Database schema and business logic
- **View:** Request handling and response generation
- **Template:** Frontend rendering and user interface

## Core Models Documentation

### User Profile Model
```python
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('designer', 'Designer'),
        ('contractor', 'Contractor'),
    )
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='client'
    )
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"
```

**Purpose:** Extends Django's built-in User model with role-based access control.

**Fields:**
- `user`: One-to-one relationship with Django User model
- `role`: User role (Client, Designer, Contractor)

**Signals:** Automatically creates UserProfile when User is created.

### Project Model
```python
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    client = models.CharField(max_length=100, null=True, blank=True)
    designer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.title
```

**Purpose:** Manages freelance projects with client assignments.

**Fields:**
- `title`: Project name/title
- `description`: Detailed project description
- `created_at`: Automatic timestamp
- `client`: Client name or identifier
- `designer`: Foreign key to User (designer assigned to project)

## Views Documentation

### Authentication Views

#### Signup View
```python
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            user_profile = UserProfile.objects.get(user=user)
            user_profile.role = role
            user_profile.save()
            return redirect("login")
    else:
        form = SignUpForm()
    return render(request, "auth/signup.html", {"form": form})
```

**Purpose:** Handles user registration with role selection.

**Process:**
1. Validates form data
2. Creates new User instance
3. Assigns role to UserProfile
4. Redirects to login page

#### Login View
```python
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "auth/login.html", {"form": form})
```

**Purpose:** Handles user authentication and session creation.

**Security Features:**
- Django's built-in AuthenticationForm
- Password hashing and verification
- Session management

### Page Views

#### Home View
```python
def home_view(request):
    return render(request, "main/home.html")
```

**Purpose:** Renders the homepage.

#### Portfolio View
```python
def portfolio(request):
    return render(request, "main/portfolio.html")
```

**Purpose:** Displays portfolio projects.

**Enhancement Opportunity:** Add project filtering and role-based display.

## Forms Documentation

### SignUpForm
```python
class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')
```

**Purpose:** Custom user registration form with role selection.

**Fields:**
- `username`: Unique username
- `email`: User email address
- `password1`: Password
- `password2`: Password confirmation
- `role`: User role selection

**Validation:**
- Django's built-in UserCreationForm validation
- Custom role field validation

## URL Configuration

### Main App URLs
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about, name='about'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
```

**URL Patterns:**
- `home`: Homepage display
- `about`: About page
- `portfolio`: Portfolio display
- `contact`: Contact information
- `signup`: User registration
- `login`: User authentication
- `logout`: User logout

## Template Structure

### Base Template
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}NightOwl Project{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">NightOwl</a>
            <div class="navbar-nav">
                {% if user.is_authenticated %}
                    <a class="nav-link" href="{% url 'logout' %}">Logout</a>
                {% else %}
                    <a class="nav-link" href="{% url 'login' %}">Login</a>
                    <a class="nav-link" href="{% url 'signup' %}">Signup</a>
                {% endif %}
            </div>
        </div>
    </nav>
    
    <main class="container mt-4">
        {% block content %}
        {% endblock %}
    </main>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### Authentication Templates

#### Signup Template
```html
{% extends 'base.html' %}

{% block title %}Signup - NightOwl Project{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h3>Create Account</h3>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <button type="submit" class="btn btn-primary">Sign Up</button>
                </form>
            </div>
            <div class="card-footer">
                <p>Already have an account? <a href="{% url 'login' %}">Login here</a></p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## Database Operations

### Migration Commands
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations

# Create specific app migration
python manage.py makemigrations nightowlmainapp
```

### Database Queries

#### User Profile Operations
```python
# Create user profile
user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
profile = UserProfile.objects.create(user=user, role='designer')

# Get user by role
designers = UserProfile.objects.filter(role='designer')

# Get projects by designer
projects = Project.objects.filter(designer=user)
```

#### Project Operations
```python
# Create project
project = Project.objects.create(
    title='New Project',
    description='Project description',
    client='Client Name',
    designer=user
)

# Get all projects
all_projects = Project.objects.all()

# Get projects by designer
designer_projects = Project.objects.filter(designer=request.user)
```

## Security Implementation

### Authentication Security
- **Password Hashing:** Django's built-in password hashing
- **CSRF Protection:** Cross-site request forgery protection
- **Session Security:** Secure session management
- **User Validation:** Form validation and sanitization

### Authorization
```python
# Role-based access control
@login_required
def designer_only_view(request):
    if request.user.userprofile.role != 'designer':
        return redirect('home')
    # Designer-specific logic
    return render(request, 'designer/dashboard.html')

# Permission decorators
from django.contrib.auth.decorators import login_required, user_passes_test

def is_designer(user):
    return user.userprofile.role == 'designer'

@user_passes_test(is_designer)
@login_required
def designer_dashboard(request):
    return render(request, 'designer/dashboard.html')
```

## Deployment Configuration

### Production Settings
```python
# settings.py
import os

# Security settings
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### Gunicorn Configuration
```bash
# gunicorn.conf.py
bind = "0.0.0.0:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
```

## Testing Framework

### Test Structure
```python
# tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import UserProfile, Project

class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            role='designer'
        )
    
    def test_user_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.role, 'designer')
    
    def test_profile_str_method(self):
        expected = 'testuser - designer'
        self.assertEqual(str(self.profile), expected)
```

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test nightowlmainapp

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## Performance Optimization

### Database Optimization
```python
# Select related and prefetch related
projects = Project.objects.select_related('designer').all()

# Database indexing
class Project(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
```

### Caching Strategy
```python
# View caching
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def portfolio_view(request):
    return render(request, "main/portfolio.html")

# Template caching
{% load cache %}
{% cache 500 sidebar %}
    <!-- Sidebar content -->
{% endcache %}
```

## API Development (Future Enhancement)

### REST API Structure
```python
# serializers.py
from rest_framework import serializers
from .models import Project, UserProfile

class ProjectSerializer(serializers.ModelSerializer):
    designer_name = serializers.CharField(source='designer.username', read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'client', 'designer_name', 'created_at']

# api_views.py
from rest_framework import viewsets
from .models import Project
from .serializers import ProjectSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
```

## Troubleshooting Guide

### Common Issues

#### Migration Errors
```bash
# Reset migrations
python manage.py migrate nightowlmainapp zero
python manage.py makemigrations nightowlmainapp
python manage.py migrate
```

#### Static File Issues
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check static file settings
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
```

#### Database Connection Issues
```python
# Test database connection
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    print("Database connection successful")
except Exception as e:
    print(f"Database connection failed: {e}")
```

### Debug Mode
```python
# Debug middleware
class DebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Debug information
        print(f"Request: {request.method} {request.path}")
        response = self.get_response(request)
        print(f"Response: {response.status_code}")
        return response
```

## Extension Ideas

### Feature Enhancements
- **Real-time Chat:** WebSocket implementation for client communication
- **Payment Integration:** Stripe/PayPal integration for project payments
- **File Upload:** Project file management and sharing
- **Notifications:** Email and in-app notification system
- **Analytics:** Project and user performance analytics

### Technical Improvements
- **API Development:** RESTful API for mobile app integration
- **Background Tasks:** Celery for asynchronous task processing
- **Search Functionality:** Advanced search with Elasticsearch
- **Performance:** Redis caching for improved performance
- **Monitoring:** Application monitoring with Sentry
