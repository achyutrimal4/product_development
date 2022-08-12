from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, authenticate, logout
from users.forms import RegistrationForm, UsersAuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.



def register_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            pass1 = form.cleaned_data.get('password1')
            authenticate_user = authenticate(email = email, password=pass1)
            if authenticate_user is not None:
                auth_login(request, authenticate_user)
                return redirect('home')
        else:
            context['registration_form'] = form
    else: #GET request
        form = RegistrationForm()
        context['registration_form'] = form
        
    return render(request, 'users/register.html', context)

def login_view(request):
    context ={}
    
    user = request.user
    if user.is_authenticated:
        return redirect('home')
    
    if request.POST:
        form = UsersAuthenticationForm(request.POST)
        if form.is_valid():
            email=request.POST['email']
            password=request.POST['password']
            
            # try:
            #     user = User.Objects.get(email=email)
            # except:
            #     messages.error(request, "User not found: %s" % email)
                
            user = authenticate(request, email=email,password=password)
            
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Username or password is incorrect')
    else:
        form=UsersAuthenticationForm()
        
    context['login_form' ]= form
    return render(request, 'users/login.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, 'User was successfully logged out.')
    return redirect('login')