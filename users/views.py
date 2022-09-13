from email import message
from lib2to3.pgen2 import token
from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from users.forms import RegistrationForm, UsersAuthenticationForm, ProfileUpdateForm, ContactForm, MessageForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Inbox
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model

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
            messages.success(
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
    User = get_user_model()
    admin = User.objects.order_by('-is_admin').first()
    context = {'user_profile': user_profile, 'admin': admin}
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


def contact(request):   
    form = ContactForm(request.POST)

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been recorded. We will get back at you as soon as possible.')
            return redirect('contact')
    context = {'form': form}
    return render(request, 'users/contact.html', context)

@login_required(login_url='login')
def create_message(request, pk):
    form = MessageForm()
    
    User = get_user_model()
    admin = User.objects.get(id=pk)
    admin_id = admin.profile.id
    admin_profile = Profile.objects.get(id=admin_id)
    recipient = admin_profile
    sender = request.user.profile
    
    if request.method == 'POST':
        form = MessageForm()
        message=form.save(commit=False)
        message.sender = sender
        message.receiver = recipient
        
        message.name = sender.name
        message.email = sender.email
        
        
        message.save()
        messages.success(request,'Password reset request was successfully sent.')
        return redirect('myprofile')
    context={'admin':admin, 'form':form, 'admin_id': admin_id}
    return render (request, 'users/messageForm.html', context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    inbox = profile.messages.all()
    inbox_count=inbox.count() 
    unread_count = inbox.filter(is_read=False).count()
    context = {'inbox': inbox, 'inbox_count':inbox_count, 'unread_count':unread_count}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    profile=request.user.profile
    inbox=profile.messages.get (id=pk)
    if inbox.is_read ==False:
        inbox.is_read= True
        inbox.save()
    context={'inbox': inbox}
    return render(request, 'users/message.html', context)