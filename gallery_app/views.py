from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from gallery_app.forms import PhotoForm
from.models import Photo, Album


# gallery pages


def gallery(request):
    photos = Photo.objects.all()
    albums = Album.objects.all()
    context = {'photos': photos, 'albums': albums}
    return render(request, 'gallery_app/gallery.html', context)


def view_photo(request, pk):
    photo = Photo.objects.get(id=pk)
    
    return render(request, 'gallery_app/photo.html', {'photo': photo})


def add_photos(request):
    form = PhotoForm()
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Photo was successfully uploaded.')
            return redirect('gallery')
    context={'form': form}
    return render(request, 'gallery_app/add_photos.html', context)
