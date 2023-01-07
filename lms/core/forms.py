from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *

class SignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2']

class LoginForm(AuthenticationForm):
     class Meta:
         model = get_user_model()
         fields = ['username', 'password']

