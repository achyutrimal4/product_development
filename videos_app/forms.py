from dataclasses import field
from django.forms import ModelForm
from .models import Video

class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ('title', 'description','video', 'tags')
        # fields = '__all__'