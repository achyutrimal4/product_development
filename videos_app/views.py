from multiprocessing import context
from pydoc import pager
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Video, Fixture, News, Standing, Players, Country
from gallery_app.models import Photo
from users.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import LiveVideoForm, VideoForm, ReviewForm, CountryForm, CategoryForm, NewsForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Q
from .utils import search_function, search_news
from django.urls import reverse_lazy, reverse




# Create your views here.
# landing page for unauthenticated users
def landing_page(request):

    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return redirect('admin_panel')
        else:
            return redirect('home')

    videos = Video.objects.all()
    fixtures = Fixture.objects.all()
    news = News.objects.all()
    standings = Standing.objects.all().order_by('-total').values()
    context = {'videos': videos, 'fixtures': fixtures,
               'news': news, 'standings': standings}
    return render(request, 'videos_app/landing_page.html', context)


# user home page
@login_required(login_url='login')
def home(request):

    videos = Video.objects.all().order_by('-uploaded').values()
    if request.method == "GET":
        videos, search_query = search_function(request)

    fixtures = Fixture.objects.all()
    news = News.objects.all()
    photos = Photo.objects.all()
    standings = Standing.objects.all().order_by('-total').values()
    players = Players.objects.all().order_by('-total').values()
    context = {'videos': videos, 'fixtures': fixtures,
               'news': news, 'standings': standings, 'search_query': search_query, 'photos': photos, 'players': players}
    return render(request, 'videos_app/home.html', context)



# add videos template
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def add_videos(request):
    page='add_video'
    form = VideoForm()
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Video was successfully uploaded.')
            return redirect("admin_panel")
    context = {'form': form, 'page': page}
    return render(request, 'videos_app/add_videos.html', context)




# add live videos
@user_passes_test(lambda u: u.is_superuser, login_url='home')
@login_required(login_url='login')
def add_live(request):
    page='add_live'
    form = LiveVideoForm()
    if request.method == 'POST':
        form = LiveVideoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Live video successfully added.')
            return redirect("admin_panel")
    context = {'liveform': form, 'page': page}
    return render(request, 'videos_app/add_videos.html', context)




# add participating countries
@user_passes_test(lambda u: u.is_superuser, login_url='home')
@login_required(login_url='login')
def add_country(request):
    page='add_country'
    form = CountryForm()
    if request.method == 'POST':
        form = CountryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Country successfully added.')
            return redirect("add_videos")
    context = {'countryform': form, 'page': page}
    return render(request, 'videos_app/add_videos.html', context)




# add sports category
@user_passes_test(lambda u: u.is_superuser, login_url='home')
@login_required(login_url='login')
def add_category(request):
    page='add_category'
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sports category successfully added.')
            return redirect("add_videos")
    context = {'categoryform': form, 'page': page}
    return render(request, 'videos_app/add_videos.html', context)


# add news
@user_passes_test(lambda u: u.is_superuser, login_url='home')
@login_required(login_url='login')
def add_news(request):
    form = NewsForm()
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'News successfully added.')
            return redirect("admin_panel")
    context = {'newsform': form}
    return render(request, 'videos_app/add_news.html', context)



# video description 
@login_required(login_url='login')
def video_desc(request, pk):
    videos = Video.objects.all()
    videoObject = Video.objects.get(id=pk)
    # video_file = get_object_or_404(Video, id=pk)
    # total_likes = video_file.total_likes()

    # category = videoObject.category().get() #extract video category from video object and use it for recommedations

    # recommendations = Video.objects.filter(Q(category__icontains=category))

    # search_query
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    videos = Video.objects.filter(Q(title__icontains=search_query) | Q(
        description__icontains=search_query))

    form = ReviewForm()

    if request.user not in videoObject.video_views.all():
        videoObject.video_views.add(request.user)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.video = videoObject
            review.comment_by = request.user.profile
            review.save()
            return HttpResponseRedirect(reverse('video_desc', args=[str(pk)]))

    views_count = videoObject.video_views.all().count()
    total_comments = videoObject.review_set.all().count()

    context = {'video': videoObject,
               'videos': videos,
               #    'recimmendation': recommendations,
               'video_views': views_count,
               'form': form,
               'total_comments': total_comments
               }
    return render(request, 'videos_app/video_desc.html', context)


# news description
@login_required(login_url='login')
def news_desc(request, pk):
    news = News.objects.all()
    newsObject = News.objects.get(id=pk)
    context = {'news': news, 'newsObject': newsObject}
    return render(request, 'videos_app/news_desc.html', context)


# admin panel
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def admin_panel(request):
    video_count = Video.objects.all().count()
    news_count = News.objects.all().count()
    users_count = User.objects.all().count()
    photo_count = Photo.objects.all().count()
    
    
    # for password reset request
    profile = request.user.profile
    inbox = profile.messages.all()
    unread_count = inbox.filter(is_read=False).count()
    
    context = {'video_count': video_count,
               'news_count': news_count, 'users_count': users_count, 'photo_count': photo_count, 'unread_count': unread_count}
    return render(request, 'videos_app/admin_panel.html', context)




# view to update videos
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def update_videos(request, pk):
    video = Video.objects.get(id=pk)
    form = VideoForm(instance=video)
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            messages.success(request, 'Video was successfully updated.')
            return redirect("admin_panel")
    context = {'form': form}
    return render(request, 'videos_app/add_videos.html', context)


# view to delete video
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def delete_videos(request, pk):
    video = Video.objects.get(pk=pk)
    if request.method == 'POST':
        video.delete()
        messages.success(request, 'Video deleted successfully')
        return redirect('home')
    context = {'object': video}
    return render(request, 'videos_app/delete_confirmation.html', context)


# like videos
def like(request, pk):
    video = get_object_or_404(Video, id=request.POST.get('video_id'))
    video.likes.add(request.user)
    return HttpResponseRedirect(reverse('video_desc', args=[str(pk)]))

# def LikeView(request, pk):
#     post = get_object_or_404(Post, id=request.POST.get('post_id'))
#     post.likes.add(request.user)
#     return redirect('score:post-detail', pk=pk)



# view all videos
@login_required(login_url='login')
def all_videos(request):
    categories = Category.objects.all()
    countries = Country.objects.all()
    # videos = Video.objects.all()
    
    # filter by category
    category = request.GET.get('category')
    if category  is None:
        videos = Video.objects.all()
    else:
        videos = Video.objects.filter(category__name = category)
    
    context = {'videos': videos, 'categories': categories, 'countries':countries}
    return render(request, 'videos_app/all_videos.html', context)



# view all news
@login_required(login_url='login')
def all_news(request):
    news = News.objects.all().order_by('-created').values()

    if request.method == "GET":
        news, search_query = search_news(request)

    context = {'news': news, 'search_query': search_query}
    return render(request, 'videos_app/all_news.html', context)


# view live games
@login_required(login_url='login')
def live_games(request):
    videos = Video.objects.all()
    context = {'videos': videos}
    return render(request, 'videos_app/live_games.html', context)


# view fixtures and results
def fixtures(request):    
    fixtures = Fixture.objects.all()
    context = {'fixtures': fixtures}
    return render(request, 'videos_app/fixtures.html', context)
