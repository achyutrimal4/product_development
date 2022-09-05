from .models import Category, Video, Country
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
                                  )
    return videos, search_query