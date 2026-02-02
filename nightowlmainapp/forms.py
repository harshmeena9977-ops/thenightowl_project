from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    ROLE_CHOICES = [
        ('', 'Select Role'),
        ('client', 'Client'),
        ('designer', 'Designer'),
        ('contractor', 'Contractor')
    ]


    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'role')