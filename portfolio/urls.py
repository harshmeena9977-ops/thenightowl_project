from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('create/', views.create_project, name='create_project'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
    path('hire/<int:project_id>/<int:designer_id>/', views.hire_designer, name='hire_designer'),
    path('complete/<int:project_id>/', views.complete_project, name='complete_project'),
    path('designer/<str:username>/', views.designer_profile, name='designer_profile'),
    path('designer/', views.designer_list, name='designer_list'),
    path('int<project_id>/', views.project_detail, name='project_detail'),
    path('<int:project_id>/apply/', views.apply_to_project, name='apply_to_project'),
    path("portfolio/<int:project_id>/apply/", views.apply_to_project, name="apply_to_project"),
    path('approve/<int:project_id>/', views.approved_projects, name='approved_project'),

]
