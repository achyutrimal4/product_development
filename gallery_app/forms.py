from django.forms import ModelForm
from django import forms
from .models import Album, Photo


class PhotoForm(ModelForm):
    class Meta:
        model=Photo
        fields = ['description', 'photo', 'album']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'description-input'}),
        }
        
class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ['name']
