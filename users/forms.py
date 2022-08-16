from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from users.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=60, help_text='Required, Add a valid email')

    class Meta:
        model = User
        fields = ("email",  "username", "full_name", "password1", "password2","country" )


class UsersAuthenticationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid email or password.")
        
