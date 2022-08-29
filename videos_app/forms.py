from dataclasses import fields
from fileinput import FileInput
from pyexpat import model
from django.forms import ModelForm
from django import forms
from .models import Video, Review


class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video', 'category', 'country']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'description-input'}),
            # 'video': forms.FileInput(attrs={'class': 'file-input'}),
            'Category': forms.SelectMultiple(attrs={'class': 'tag-input'}),
        }
        # fields = '__all__'


class ReviewForm (ModelForm):
    class Meta:
        model = Review
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'comment-input', 'placeholder': 'Add a comment'}),           
        }
