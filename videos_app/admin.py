from django.contrib import admin
from .models import Video, Review, Category, Fixture, News, Standing, Country, Players, LiveVideo

# Register your models here.
admin.site.register(Video)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Fixture)
admin.site.register(News)
admin.site.register(Standing)
admin.site.register(Country)
admin.site.register(Players)
admin.site.register(LiveVideo)
