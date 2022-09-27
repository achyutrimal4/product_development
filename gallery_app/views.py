from videos_app.utils import search_photos
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from gallery_app.forms import PhotoForm, AlbumForm
from .models import Photo, Album


# gallery pages


def gallery(request):
    album = request.GET.get('album')

    if request.method == "GET":
        photos, search_query = search_photos(request)

    if album == None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(album__name=album)

    albums = Album.objects.all()
    # photos = Photo.objects.all()

    # search query

    context = {'photos': photos, 'albums': albums,
               'search_query': search_query}
    return render(request, 'gallery_app/gallery.html', context)


def view_photo(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'gallery_app/photo.html', {'photo': photo})


def add_photos(request):
    page = 'add_photo'
    form = PhotoForm()
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Photo was successfully uploaded.')
            return redirect('gallery')
    context = {'form': form, 'page': page}
    return render(request, 'gallery_app/add_photos.html', context)


def add_album(request):
    page = 'add_album'
    form = AlbumForm()
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New album successfully created.')
            return redirect('add_photos')
    context = {'albumform': form, 'page': page}
    return render(request, 'gallery_app/add_photos.html', context)
