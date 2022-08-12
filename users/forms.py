from dataclasses import field
import email
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from users.models import User
from django_countries.fields import CountryField


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required, Add a valid email')
    
    class Meta:
        model=User
        country =forms.CharField(widget=forms.TextInput(attrs={'class': 'countryfield'}))
        fields=("email", "full_name","username",  "password1", "password2", "country")
        

class UsersAuthenticationForm(forms.ModelForm):
    password    = forms.CharField(widget=forms.PasswordInput, label='Password')
    
    class Meta:
        model=User
        fields = ('email', 'password')
        
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid email or password.")