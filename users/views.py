from email import message
from lib2to3.pgen2 import token
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from users.forms import RegistrationForm, UsersAuthenticationForm, ProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test

from verify_email.email_handler import send_verification_email


def register_view(request):

    user = request.user
    if user.is_authenticated:
        return redirect('home')

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
            messages.info(
                request, 'Account created. Please check your inbox and verify your email to continue.')
            return redirect('login')
        else:
            context['registration_form'] = form
    else:  # GET request
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'users/register.html', context)


def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return redirect('admin_panel')
        else:
            return redirect('home')

    if request.method == "POST":
        form = UsersAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    if user.is_superuser:
                        return redirect('admin_panel')
                    else:
                        return redirect('home')
                else:
                    messages.error(request, 'Please verify your email address to login.')

    else:
        form = UsersAuthenticationForm()

    context['login_form'] = form
    return render(request, 'users/login.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, 'User was successfully logged out.')
    return redirect('landing_page')


@login_required(login_url='login')
def profile_view(request):
    user_profile = request.user.profile
    context = {'user_profile': user_profile}
    return render(request, 'users/users_profile.html', context)


@login_required(login_url='login')
def edit_profile(request):
    profile = request.user.profile
    form = ProfileUpdateForm(instance=profile)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('myprofile')
    context = {'form': form}
    return render(request, 'users/editProfile.html', context)
