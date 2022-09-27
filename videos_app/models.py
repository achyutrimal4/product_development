from pickle import FALSE
from unicodedata import category
from django.db import models
from users.models import User
from users.models import Profile
import uuid
import datetime
from django_countries.fields import CountryField

from django.conf import settings

# Create your models here.


class Video (models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    video = models.FileField(upload_to="videos/", null=True)
    upload_by = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ManyToManyField(
        'Category', blank=False, verbose_name="Sports Category")
    country = models.ManyToManyField(
        'Country', blank=False, verbose_name="Participating Countries")
    likes = models.ManyToManyField(
        User, blank=True, related_name='video_posts')
    video_views = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='video_views', blank=True, default="admin@gmail.com")
    uploaded = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.title


class LiveVideo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    url = models.TextField(verbose_name="Live URL")
    upload_by = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ManyToManyField(
        'Category', blank=True, verbose_name="Sports Category")
    country = models.ManyToManyField(
        'Country', blank=True, verbose_name="Participating Countries")
    venue = models.CharField(max_length=255, blank=True,
                             null=True, default="Bayjing FunOlympics Park")
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name='like_live')
    video_views = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_views', blank=True, default="admin@gmail.com")
    uploaded = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.title


class Review(models.Model):
    comment_by = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.comment


class LiveComments(models.Model):
    comment_by = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True)
    video = models.ForeignKey(LiveVideo, on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.comment


class Category (models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name


class Country (models.Model):
    country = CountryField(blank=False, null=False,
                           verbose_name="Participating Country", blank_label="Select Country")
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.country)


class News (models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/news/')
    imageBy = models.CharField(max_length=200, default="Funolympics Admin")
    author = models.CharField(
        max_length=200, default="Funolympics Admin", null=True, blank=True)
    photo_caption = models.CharField(max_length=255, null=True, blank=True)
    category = models.ManyToManyField(
        'Category', blank=True, verbose_name="News Category")
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.title


class Fixture (models.Model):
    fixture = models.CharField(max_length=200)
    date = models.DateField(verbose_name='Game Date')
    thumbnail = models.ImageField(
        upload_to='images/fixtures/', default='media/images/background/bg.png', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.fixture


class Standing (models.Model):
    country = models.CharField(max_length=200, unique=True)
    gold = models.IntegerField()
    silver = models.IntegerField()
    bronze = models.IntegerField()
    total = models.IntegerField()

    def __str__(self):
        return self.country


class Player(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(
        null=True, blank=True, upload_to='images/players/', default='images/profile_pics/default.jpg')
    gold = models.IntegerField()
    silver = models.IntegerField()
    bronze = models.IntegerField()
    total = models.IntegerField()

    def __str__(self):
        return self.name
