from django.urls import path, include
from . import views
from django.conf import settings 
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    # 🏠 Public Pages
    path('admin/', admin.site.urls),   # ✅ only once

    path('', views.home_view, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('portfolio/', include('portfolio.urls')),
    path('chat/', include('chat.urls')),   # ✅ fixed with trailing slash

    # 🔐 Authentication
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    # 📊 Dashboards
    path('dashboard/client/', views.client_dashboard, name='client_dashboard'),
    path('dashboard/designer/', views.designer_dashboard, name='designer_dashboard'),
    path('dashboard/contractor/', views.contractor_dashboard, name='contractor_dashboard'),
]



