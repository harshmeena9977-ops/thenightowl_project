from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

from .forms import SignUpForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from portfolio.services import get_projects_by_client


# Home Page
def home_view(request):
    return render(request, "main/home.html")

# About Page
def about(request):
    return render(request, "main/about.html")

# Portfolio Page
def portfolio(request):
    return render(request, "main/portfolio.html")

# Contact Page
def contact(request):
    return render(request, "main/contact.html")

# Signup Page
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

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            role = getattr(user.userprofile, "role", "").lower()

            if role == "client":
                return redirect("client_dashboard")
            elif role == "designer":
                return redirect("designer_dashboard")
            elif role == "contractor":
                return redirect("contractor_dashboard")
            else:
                return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "auth/login.html", {"form": form})


# Logout
def logout_view(request):
    logout(request)
    return redirect("home")

from portfolio.models import Project

# Client Dashboard
@login_required
def client_dashboard(request):
    projects = get_projects_by_client(request.user)
    return render(request, "dashboards/client.html", {"projects": projects})

# Designer Dashboard
from portfolio.models import ProjectApplication

@login_required
def designer_dashboard(request):
    applications = ProjectApplication.objects.filter(designer=request.user)
    projects = [app.project for app in applications]
    return render(request, 'dashboards/designer.html', {'projects': projects})


# Contractor Dashboard
def contractor_dashboard(request):
    projects = Project.objects.filter(designer=request.user)
    return render(request, "dashboards/contractor.html", {"projects": projects})

from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse


from django.shortcuts import render

def landing_page(request):
    return render(request, 'nightowlmainapp/landing.html')


# Marketplace homepage 
def marketplace_home(request): 
    return HttpResponse("Marketplace Home Page")

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project

@login_required(login_url='login')
def complete_project(request, project_id):
    project = get_object_or_404(
        Project,
        id=project_id,
        assigned_designer=request.user
    )

    project.status = 'completed'
    project.save()

    return redirect('designer_dashboard')

from django.shortcuts import render

def create_portfolio(request):
    if request.method == "POST":
        # yahan tum form save kar sakte ho
        pass
    return render(request, 'nightowlmainapp/portfolio_form.html')

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'portfolio/project_list.html', {'projects': projects})

