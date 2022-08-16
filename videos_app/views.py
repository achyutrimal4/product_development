import http
from django.shortcuts import render, redirect
from .models import Video
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import VideoForm
from django.contrib import messages



# Create your views here.
@login_required(login_url ='login')
def home(request):
    videos = Video.objects.all()
    context={'videos': videos}
    return render(request, 'videos_app/home.html', context)

@login_required(login_url ='login')
def video_desc(request, pk):
    videoObject = Video.objects.get(id=pk)
    context={'video':videoObject}
    return render(request, 'videos_app/video_desc.html', context)

@login_required(login_url ='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def admin_panel(request):
    return render(request, 'videos_app/admin_panel.html')

@login_required(login_url ='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def add_videos(request):
    form = VideoForm()
    
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success  (request, 'Video was successfully uploaded.')
            return redirect("admin_panel")         
    context={'form': form}
    return render(request, 'videos_app/add_videos.html', context)

@login_required(login_url ='login')
@user_passes_test(lambda u: u.is_superuser, login_url='home')
def update_videos(request, pk):
    video = Video.objects.get(pk=pk)
    form = VideoForm(instance=video)
    
    
    if request.method == 'POST':
        form = VideoForm(request.POST, instance=video)
        if form.is_valid():
            form.save()
            messages.success  (request, 'Video was successfully updated.')
            return redirect("admin_panel")         
    context={'form': form}
    return render(request, 'videos_app/add_videos.html', context)
  
  
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