from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from portfolio.models import Project

@login_required
def project_chat(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    # Only client or assigned designer allowed
    if request.user not in [project.client, project.assigned_designer]:
        return redirect('home')
    
    # ✅ use 'created' instead of 'timestamp'
    messages = Message.objects.filter(project=project).order_by('created')
    
    if request.method == 'POST':
        text = request.POST.get('message')
        if text:
            # ✅ use 'text' instead of 'content'
            Message.objects.create(
                project=project,
                sender=request.user,
                text=text
            )
        return redirect('project_chat', project_id=project.id)
    
    return render(request, 'chat/project_chat.html', {
        'project': project,
        'messages': messages
    })
