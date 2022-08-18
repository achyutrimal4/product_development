from django.contrib import admin
from .models import Video, Review, Tag, Fixture, News, Standing

# Register your models here.
admin.site.register(Video)
admin.site.register(Review)
admin.site.register(Tag)
admin.site.register(Fixture)
admin.site.register(News)
admin.site.register(Standing)
