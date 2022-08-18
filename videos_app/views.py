from django.shortcuts import render, redirect
from .models import Video, Fixture, News, Standing
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import VideoForm
from django.contrib import messages



# Create your views here.

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
    videoObject = Video.objects.get(id=pk)
    context={'video':videoObject}
    return render(request, 'videos_app/video_desc.html', context)


# admin panel
@login_required(login_url ='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def admin_panel(request):
    return render(request, 'videos_app/admin_panel.html')



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
    context={'form': form}
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



