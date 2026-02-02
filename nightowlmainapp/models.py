from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver   

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

from django.db import models
from django.contrib.auth.models import User   # Django ka built-in User model

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    client = models.CharField(max_length=100, null=True, blank=True)

    # ✅ Add designer field (ForeignKey to User)
    designer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)