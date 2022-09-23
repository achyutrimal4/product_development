from gallery_app.models import Album, Photo
from .models import Category, Fixture, Video, Country, News
from django.db.models import Q


def search_function(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        
    category = Category.objects.filter(name__icontains = search_query) 
    country = Country.objects.filter(country__icontains = search_query)
    videos = Video.objects.distinct().filter(Q(title__icontains=search_query)|
                                  Q(description__icontains=search_query)|
                                  Q(category__in = category)|
                                  Q(country__in = country)                                  
                                  ).order_by('-uploaded')
    return videos, search_query

def search_news(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        
    category = Category.objects.filter(name__icontains = search_query) 
    news = News.objects.distinct().filter(Q(title__icontains=search_query)|
                                  Q(description__icontains=search_query)|
                                  Q(category__in = category)
                                  ).order_by('-created')
    
    return news, search_query


def search_photos(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        
    album = Album.objects.filter(name__icontains = search_query) 
    photo = Photo.objects.distinct().filter(
                                  Q(description__icontains=search_query)|
                                  Q(album__in = album)
                                  ).order_by('-uploaded')
    
    return photo, search_query


def search_fixtures(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        
    # fixture = Fixture.objects.filter(fixture__icontains = search_query) 
    fixture = Fixture.objects.distinct().filter(
                                  Q(fixture__icontains=search_query)
                                  ).order_by('-created')
    
    return fixture, search_query