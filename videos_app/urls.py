from django.urls import path
from . import views

urlpatterns=[
   path('',views.landing_page, name='landing_page'),
   path('home/', views.home, name="home"),
   path('video-description/<str:pk>/', views.video_desc, name="video_desc"),
   path('admin-panel/', views.admin_panel, name="admin_panel"),
   path('add-videos/', views.add_videos, name="add_videos"),
   path('update-videos/<str:pk>/', views.update_videos, name="update_videos"),
   path('delete-videos/<str:pk>/', views.delete_videos, name="delete_videos"),
]
