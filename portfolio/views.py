from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from portfolio.models import Project, ProjectApplication
from wallets.models import Wallet
from .forms import ProjectForm
# Create your views here.

def portfolio(request):
    projects = Project.objects.all()
    return render(request, "portfolio/project_list.html", {"projects": projects})




def project_list(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'portfolio/project_list.html', {
        'projects': projects
    })
    

@login_required
def designer_portfolio(request):
    projects = Project.objects.filter(designer=request.user)
    return render(request, 'portfolio/designer_portfolio.html', {
        'projects': projects
    })

@login_required(login_url='login')
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user
            project.status = 'open'
            project.save()
            return redirect('client_dashboard')
    else:
        form = ProjectForm()

    return render(request, 'portfolio/create_project.html', {'form': form})

from django.shortcuts import render, get_object_or_404
from .models import Project

def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    applications = project.applications.all()
    return render(request, 'portfolio/project_detail.html', {
        'project': project,
        'applications': applications
    })
    
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectApplication

@login_required(login_url='login')
def apply_to_project(request, project_id):
    print("APPLY NEW HIT ")
    project = get_object_or_404(Project, id=project_id)
    
    print("APPlY TO PROJECT CALLED", request.user.username)

    # Sirf designer hi apply kare
    if request.user.userprofile.role != 'designer':
        print("NOT A DESIGNER")
        return redirect('project_detail', project_id=project_id)

    obj, created = ProjectApplication.objects.get_or_create(
        project=project,
        designer=request.user
    )
    print("APPLICATION CREATED:", created)
    return redirect('project_detail', project_id=project_id)


from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectApplication

@login_required(login_url='login')
def hire_designer(request, project_id, designer_id):
    project = get_object_or_404(Project, id=project_id, client=request.user)

    # Project already hired
    if project.status != 'open':
        return redirect('client_dashboard')
    


    designer = get_object_or_404(ProjectApplication,
                                 project=project,
                                 designer_id=designer_id)

    application = get_object_or_404(
        ProjectApplication,
        project=project,
        designer_id=designer_id
    )

    # Assign designer
    project.assigned_designer = application.designer
    project.status = 'in_progress'
    project.save()

    # Reject others
    ProjectApplication.objects.filter(
        project=project
    ).exclude(designer=application.designer).delete()

    return redirect('client_dashboard')


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

from .models import DesignerProfile, Project
from django.shortcuts import render, get_object_or_404

# views.py
def designer_profile(request, username):
    designer = get_object_or_404(DesignerProfile, user__username=username)
    skills_list = designer.skills.split(",")  # split here
    return render(request, "portfolio/designer_profile.html", {
        "designer": designer,
        "skills_list": skills_list
    })

def designer_list(request):
    designers = DesignerProfile.objects.all()
    return render(request, "portfolio/designer_list.html", {
        "designers": designers
    })
    
@login_required
def client_dashboard(request):
    projects = Project.objects.filter(client=request.user)
    return render(request, 'dashboards/client.html', {
        'projects': projects
    })
    
@login_required
def approved_projects(request, project_id):
    project = get_object_or_404(Project, id=project_id, client=request.user, status='completed')

    wallet, created = Wallet.objects.get_or_create(user=request.user)
    wallet.balance += project.budget
    wallet.save()

    project.status = 'paid'
    project.save()

    return redirect('client_dashboard')

