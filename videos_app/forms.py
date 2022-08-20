from dataclasses import field
from fileinput import FileInput
from django.forms import ModelForm
from django import forms
from .models import Video

class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description','video', 'category', 'country']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'description-input'}),
            # 'video': forms.FileInput(attrs={'class': 'file-input'}),
            'Category': forms.SelectMultiple (attrs={'class': 'tag-input'}),
        }
        # fields = '__all__'
        
