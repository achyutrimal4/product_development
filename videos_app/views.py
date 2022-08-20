from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from .models import Video, Fixture, News, Standing
from users.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import VideoForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse



# Create your views here.
#landing page for unauthenticated users
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
    context={'videos': videos, 'fixtures': fixtures, 'news': news, 'standings': standings}
    return render(request, 'videos_app/landing_page.html', context)
    

# user home page
@login_required(login_url ='login')
def home(request):
    videos = Video.objects.all()
    fixtures = Fixture.objects.all()
    news = News.objects.all()
    standings = Standing.objects.all().order_by('-total').values()
    context={'videos': videos, 'fixtures': fixtures, 'news': news, 'standings': standings}
    return render(request, 'videos_app/home.html', context)


# video description and play 
@login_required(login_url ='login')
def video_desc(request, pk):
    videos = Video.objects.all()
    videoObject = Video.objects.get(id=pk)
    video_file = get_object_or_404(Video, id=pk)
    # total_likes = video_file.total_likes()
    context={'video':videoObject, 'videos':videos}
    return render(request, 'videos_app/video_desc.html', context)

@login_required(login_url ='login')
def news_desc(request, pk):
    news = News.objects.all()
    newsObject = News.objects.get(id=pk)
    context={'news':news, 'newsObject':newsObject}
    return render(request, 'videos_app/news_desc.html', context)

# admin panel
@login_required(login_url ='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def admin_panel(request):
    video_count = Video.objects.all().count()
    news_count = News.objects.all().count()
    users_count = User.objects.all().count()
    context={'video_count': video_count, 'news_count': news_count, 'users_count': users_count}
    return render(request, 'videos_app/admin_panel.html', context)



# add videos template
@login_required(login_url ='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def add_videos(request):     
    form = VideoForm()    
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success  (request, 'Video was successfully uploaded.')
            return redirect("admin_panel")         
    context={'add_video_form': form}
    return render(request, 'videos_app/add_videos.html', context)



# view to update videos
@login_required(login_url ='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def update_videos(request, pk):
    video = Video.objects.get(pk=pk)
    form = VideoForm(instance=video)    
    
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            messages.success  (request, 'Video was successfully updated.')
            return redirect("admin_panel")         
    context={'form': form}
    return render(request, 'videos_app/add_videos.html', context)
  
  
  
# view to delete video
@login_required(login_url ='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def delete_videos(request, pk):
    video = Video.objects.get(pk=pk)
    if request.method == 'POST':
        video.delete()
        messages.success(request, 'Video deleted successfully')
        return redirect('home')
    context={'object':video}
    return render(request, 'videos_app/delete_confirmation.html', context)

def like(request, pk):
    video = get_object_or_404(Video, id=request.POST.get('video_id'))
    video.likes.add(request.user)
    return HttpResponseRedirect(reverse('video_desc', args=[str(pk)]))

# def LikeView(request, pk):
#     post = get_object_or_404(Post, id=request.POST.get('post_id'))
#     post.likes.add(request.user)
#     return redirect('score:post-detail', pk=pk)
