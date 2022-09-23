from django.urls import path
from . import views

urlpatterns=[
    # user app
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('logout/', views.logout_view, name='logout'),
    path('my_profile/', views.profile_view, name='myprofile'),
    path('edit_profile/', views.edit_profile, name='editprofile'),
    
    # send message
    path('inbox/', views.inbox, name='inbox'),
    path('view-message/<str:pk>/', views.viewMessage, name='viewMessage'),
    path('create-message/<str:pk>/', views.create_message, name='create-message'),
    # create-message/<str:pk>/ --> id of the account to which the message is being sent
    
    # delete message
    path('delete-inbox/<str:pk>/', views.delete_reset_inbox, name="delete-inbox"),

    
    # view and respond to contact messages
    path('contact/', views.contact, name='contact'),
    path('contact-inbox/', views.contact_inbox, name='contact-inbox'),
    path('view-contact-mail/<str:pk>',views.viewContactMail, name='view-contact-mail'),
    
    # change password
    path('change-password/', views.change_password, name='change-password'),
    

]