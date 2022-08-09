from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
# Create your views here.

def login(request):
    return render(request, 'users/login.html')

def signup(request):
    return render(request, 'users/signup.html')