from django.urls import path
from . import views

urlpatterns=[
    path('', views.login, name='login'),
    path('users/register', views.register_view, name='register'),
]