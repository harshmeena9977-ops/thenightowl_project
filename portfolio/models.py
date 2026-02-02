from django.db import models
from django.conf import settings

from django.db import models
from django.conf import settings

class Project(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    budget = models.IntegerField()

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_projects'
    )

    assigned_designer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_projects'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('client', 'title')

    def __str__(self):
        return f"{self.client.username} → {self.title}"

class Portfolio(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='portfolio_images/', blank=True, null=True)

    def __str__(self):
        return self.title

from django.db import models
from django.conf import settings

class ProjectApplication(models.Model):
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name="applications"   # 👈 ये जोड़ दो
    )
    designer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'designer')

    def __str__(self):
        return f"{self.designer.username} → {self.project.title}"



from django.contrib.auth.models import User

class DesignerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    bio = models.TextField()
    skills = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='designers/', blank=True, null=True)

    def __str__(self):
        return self.user.username