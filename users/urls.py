from django.urls import path
from . import views

urlpatterns=[
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('logout/', views.logout_view, name='logout'),
    path('my_profile/<str:pk>', views.profile_view, name='myprofile'),
    path('edit_profile/<str:pk>', views.edit_profile, name='editprofile'),
]