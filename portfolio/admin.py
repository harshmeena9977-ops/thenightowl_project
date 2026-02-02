from django.contrib import admin
from .models import Project, Portfolio, ProjectApplication
from .models import DesignerProfile

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'assigned_designer', 'status', 'budget', 'created_at']
    list_filter = ['client', 'assigned_designer', 'status', 'created_at']

# ✅ Register only once with ProjectAdmin
admin.site.register(Project, ProjectAdmin)
admin.site.register(Portfolio)
admin.site.register(ProjectApplication)
admin.site.register(DesignerProfile)

