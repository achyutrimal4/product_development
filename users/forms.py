from dataclasses import field
from fileinput import FileInput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from users.models import Inbox, User, Profile, ContactMail, ContactReply


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'autocomplete': False}))
    # email = forms.EmailField(max_length=60, help_text='Required, Add a valid email', )

    class Meta:
        model = User
        fields = ("email",  "username", "full_name", "password1",
                  "password2", "country", "phone_number")


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


class ProfileUpdateForm(forms.ModelForm):
    profile_image = forms.FileField()

    class Meta:
        model = Profile
        fields = ('username', 'name', 'country',
                  'profile_image', 'phone_number')


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMail
        fields = ('email', 'subject', 'message')
        widgets = {
            'message': forms.Textarea(attrs={'class': 'description-input'}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Inbox
        fields = ['subject']


class ContactReplyForm(forms.ModelForm):
    class Meta:
        model = ContactReply
        fields = ('receiver', 'message',)
        widgets = {
            'receiver': forms.EmailInput(attrs={'placeholder': 'Receiver email address'}),
            'message': forms.Textarea(attrs={'class': 'description-input'}),
        }

