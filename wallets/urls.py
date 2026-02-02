from django.urls import path
from . import views

urlpatterns = [
    # Define your wallet-related URL patterns here
    
    path('', views.wallet_dashboard, name='wallet_dashboard'),
    path('withdraw/', views.withdraw_funds, name='withdraw_funds'),
]
