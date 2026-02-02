from .models import Project

def get_projects_by_client(user):
    return Project.objects.filter(client=user)