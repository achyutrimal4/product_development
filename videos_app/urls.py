from django.urls import path
from . import views

urlpatterns=[
   # app 
   path('',views.landing_page, name='landing_page'),
   path('home/', views.home, name="home"),
   path('admin-panel/', views.admin_panel, name="admin_panel"),
   
   # video 
   path('add-videos/', views.add_videos, name="add_videos"),
   path('video-description/<str:pk>/', views.video_desc, name="video_desc"),
   path('update-videos/<str:pk>/', views.update_videos, name="update_videos"),
   path('delete-videos/<str:pk>/', views.delete_videos, name="delete_videos"),
   path('all-videos/', views.all_videos, name="all_videos"),
   path('like/<str:pk>/', views.like, name="like_video"),
   path('live-games/', views.live_games, name="live_games"),
   path('add-live/',views.add_live, name='add_live'),
   
   
   path('add-country/', views.add_country, name='add_country'),
   path('add-category/', views.add_category, name='add_category'),
   
   # fixtures
   path('fixtures/', views.fixtures, name='fixtures'),
   
   # news
   path('all-news/', views.all_news, name='all_news'),
   path('news-description/<str:pk>/', views.news_desc, name="news_desc"),
   path('add-news/',views.add_news, name='add_news'),
   
   # add misc
   path('add-fixtures/', views.add_fixtures, name='add_fixtures'),
   path('add-players/', views.add_players, name='add_players'),
   path('add-standings/', views.add_standing, name='add_standings'),
   
]
 