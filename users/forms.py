from dataclasses import field
import email
from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required, Add a valid email')
    
    class Meta:
        model=User
        fields=("email", "username", "password1", "password2")