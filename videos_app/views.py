from multiprocessing import context
from operator import is_
from pickle import FALSE
from pydoc import pager
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Video, Fixture, News, Standing, Player, Country, LiveVideo
from gallery_app.models import Photo
from users.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import FixtureForm, LiveVideoForm, PlayerForm, StandingForm, VideoForm, ReviewForm, CountryForm, CategoryForm, NewsForm, LiveCommentsForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Q
from .utils import search_fixtures, search_function, search_live, search_news, search_photos
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

    photos = Photo.objects.all().order_by('-uploaded')
    players = Player.objects.all().order_by('-total')[0:5]
    live = LiveVideo.objects.all().order_by('-uploaded').first()

    videos = Video.objects.all()
    fixtures = Fixture.objects.all()
    news = News.objects.all()
    standings = Standing.objects.all().order_by('-total').values()
    context = {'videos': videos,
               'fixtures': fixtures,
               'news': news,
               'standings': standings,
               'photos': photos,
               'players': players,
               'live': live, }
    return render(request, 'videos_app/landing_page.html', context)


# user home page
@login_required(login_url='login')
def home(request):

    videos = Video.objects.all().order_by('-uploaded').values()
    if request.method == "GET":
        videos, search_query = search_function(request)

    news = News.objects.all().order_by('-created')
    if request.method == "GET":
        news, search_query = search_news(request)

    photos = Photo.objects.all().order_by('-uploaded')
    if request.method == "GET":
        photos, search_query = search_photos(request)

    fixtures = Fixture.objects.all().order_by('-created')[0:6]
    standings = Standing.objects.all().order_by('-total')[0:7]
    players = Player.objects.all().order_by('-total')[0:5]
    live = LiveVideo.objects.all().order_by('-uploaded').first()
    context = {'videos': videos,
               'fixtures': fixtures,
               'news': news,
               'standings': standings,
               'search_query': search_query,
               'photos': photos,
               'players': players,
               'live': live,
               }
    return render(request, 'videos_app/home.html', context)


# add videos template
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def add_videos(request):
    page = 'add_video'
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
    page = 'add_live'
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
    page = 'add_country'
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
    page = 'add_category'
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


# =============================================================
# Add misc(fixtures, players, and latest standings)
@user_passes_test(lambda u: u.is_superuser, login_url='home')
@login_required(login_url='login')
def add_fixtures(request):
    page = 'add_fixtures'
    form = FixtureForm()
    if request.method == 'POST':
        form = FixtureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fixture successfully added.')
            return redirect("admin_panel")
    context = {'fixtureform': form, 'page': page}
    return render(request, 'videos_app/add_misc.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='home')
@login_required(login_url='login')
def add_players(request):
    page = 'add_players'
    form = PlayerForm()
    if request.method == 'POST':
        form = PlayerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Player successfully added.')
            return redirect("admin_panel")
    context = {'playerform': form, 'page': page}
    return render(request, 'videos_app/add_misc.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='home')
@login_required(login_url='login')
def add_standing(request):
    page = 'add_standing'
    form = StandingForm()
    if request.method == 'POST':
        form = StandingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Standing successfully updated.')
            return redirect("admin_panel")
    context = {'standingform': form, 'page': page}
    return render(request, 'videos_app/add_misc.html', context)


# video description
@login_required(login_url='login')
def video_desc(request, pk):
    videos = Video.objects.all()

    videoObject = Video.objects.get(id=pk)
    total_likes = videoObject.likes.count()

    liked = False
    if videoObject.likes.filter(id=request.user.id).exists():
        liked = True

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
               'video_views': views_count,
               'form': form,
               'total_comments': total_comments,
               'total_likes': total_likes,
               'liked': liked
               }
    return render(request, 'videos_app/video_desc.html', context)


# news description
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

    contact_mails = profile.contact_mails.all()
    unread_mails = contact_mails.filter(is_read=False).count()

    context = {'video_count': video_count,
               'news_count': news_count, 'users_count': users_count, 'photo_count': photo_count,
               'unread_count': unread_count,
               'unread_mails': unread_mails, }
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
    liked = False
    if video.likes.filter(id=request.user.id).exists():
        video.likes.remove(request.user)
        liked = False
    else:
        video.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('video_desc', args=[str(pk)]))

def like_live(request, pk):
    video = get_object_or_404(LiveVideo, id=request.POST.get('video_id'))
    liked = False
    if video.likes.filter(id=request.user.id).exists():
        video.likes.remove(request.user)
        liked = False
    else:
        video.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('live_desc', args=[str(pk)]))


# view all videos
@login_required(login_url='login')
def all_videos(request):
    categories = Category.objects.all()
    countries = Country.objects.all()
    # videos = Video.objects.all()

    # search query
    if request.method == "GET":
        videos, search_query = search_function(request)

    # filter by category
    category = request.GET.get('category')
    if category:
        if category is None:
            videos = Video.objects.all()
        else:
            videos = Video.objects.filter(category__name=category)

    context = {'videos': videos,  'search_query': search_query,
               'categories': categories, 'countries': countries}
    return render(request, 'videos_app/all_videos.html', context)


# view all news
def all_news(request):
    news = News.objects.all().order_by('-created').values()
    categories = Category.objects.all()
    
         
    if request.method == "GET":
        news, search_query = search_news(request)

    category = request.GET.get('category')
    if category:
        if category is None:
            news = News.objects.all()
        else:
            news = News.objects.filter(category__name=category)      
   

    context = {'news': news, 'search_query': search_query,
               'categories': categories, }
    return render(request, 'videos_app/all_news.html', context)


# view live games
@login_required(login_url='login')
def live_games(request):
    live_videos = LiveVideo.objects.all()
    
    if request.method == "GET":
        live_videos, search_query = search_live(request)
        
    context = {'live_videos': live_videos, 'search_query': search_query,}
    return render(request, 'videos_app/live_games.html', context)

# video description


@login_required(login_url='login')
def live_desc(request, pk):
    live_videos = LiveVideo.objects.all()

    liveVideoObject = LiveVideo.objects.get(id=pk)

    total_likes = liveVideoObject.likes.count()
    liked = False
    if liveVideoObject.likes.filter(id=request.user.id).exists():
        liked=True

    # search_query
    search_query = ''
    # if request.GET.get('search_query'):
    #     search_query = request.GET.get('search_query')

    # videos = Video.objects.filter(Q(title__icontains=search_query) | Q(
    #     description__icontains=search_query))

    form = LiveCommentsForm()

    if request.user not in liveVideoObject.video_views.all():
        liveVideoObject.video_views.add(request.user)

    if request.method == 'POST':
        form = LiveCommentsForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.video = liveVideoObject
            review.comment_by = request.user.profile
            review.save()
            return HttpResponseRedirect(reverse('live_desc', args=[str(pk)]))

    views_count = liveVideoObject.video_views.all().count()
    total_comments = liveVideoObject.livecomments_set.all().count()

    context = {'video': liveVideoObject,
               'videos': live_videos,
               'form': form,
                  'video_views': views_count,
                  'total_comments': total_comments,
                  'total_likes':total_likes,
                  'liked':liked
               }
    return render(request, 'videos_app/live_desc.html', context)

# view fixtures and results


def fixtures(request):
    page = 'fixtures'
    fixtures = Fixture.objects.all()

    # search query
    if request.method == "GET":
        fixtures, search_query = search_fixtures(request)

    context = {'fixtures': fixtures, 'page': page,
               'search_query': search_query}
    return render(request, 'videos_app/fixtures_results.html', context)


def results(request):
    page = 'results'
    standings = Standing.objects.all().order_by('-total')
    players = Player.objects.all().order_by('-total')
    context = {'standings': standings, 'page': page, 'players': players}
    return render(request, 'videos_app/fixtures_results.html', context)


# =============================================================
# Analytics
# ===============================



