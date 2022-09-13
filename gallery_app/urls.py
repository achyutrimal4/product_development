from django.urls import path
from . import views


urlpatterns = [
# gallery
path('gallery/', views.gallery, name="gallery"),
path('add-photos/', views.add_photos, name="add_photos"),
path('view-photo/<str:pk>/', views.view_photo, name="view_photo"),    
path('add-album', views.add_album, name="add_album"),
]
