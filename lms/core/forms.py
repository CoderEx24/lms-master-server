from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class CustomerSignupForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['username', 'password1', 'password2']

