from django.contrib import admin
from .models import Video, Review, Tag

# Register your models here.
admin.site.register(Video)
admin.site.register(Review)
admin.site.register(Tag)