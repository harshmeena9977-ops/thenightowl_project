from django.urls import path
from . import views

urlpatterns = [
    path('chatproject/<int:project_id>/', views.project_chat, name='project_chat'),
]
