import email
from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, authenticate
from users.forms import RegistrationForm
# Create your views here.

def login(request):
    return render(request, 'users/login.html')

# def register(request):
#     return render(request, 'users/register.html')

def register_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            pass1 = form.cleaned_data.get('password1')
            authenticate_user = authenticate(email = email, password=pass1)
            auth_login(request, authenticate_user)
            return redirect('home')
        else:
            context['registration_form'] = form
    else: #GET request
        form = RegistrationForm()
        context['registration_form'] = form
        
    return render(request, 'users/register.html', context)