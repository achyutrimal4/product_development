from django.contrib import admin
from .models import Video, Review, Category, Fixture, News, Standing

# Register your models here.
admin.site.register(Video)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Fixture)
admin.site.register(News)
admin.site.register(Standing)
