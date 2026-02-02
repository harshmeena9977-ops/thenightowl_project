from django.db import models
from django.conf import settings
from portfolio.models import Project
from django.utils import timezone

class ChatRoom(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='u1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='u2', on_delete=models.CASCADE)

    def __str__(self):
        return f"ChatRoom between {self.user1} and {self.user2}"

class Message(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=1)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(default=timezone.now)





    def __str__(self):
        return f"{self.sender}: {self.text[:20]}"

