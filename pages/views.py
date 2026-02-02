
# Create your views here.
from django.shortcuts import render

def home(request):
    return render(request, 'pages/home.html')

def terms(request):
    return render(request, 'pages/terms.html')