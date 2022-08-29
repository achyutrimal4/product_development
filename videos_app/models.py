from email.policy import default
from re import T
from django.db import models
from users.models import User
from users.models import Profile
import uuid
import datetime
from django.conf import settings

# Create your models here.


class Video (models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    video = models.FileField(upload_to="videos/", null=True)
    upload_by = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ManyToManyField(
        'Category', blank=True, verbose_name="Sports Category")
    country = models.ManyToManyField(
        'Country', blank=True, verbose_name="Participating Countries")
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name='video_posts')
    video_views = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='video_views', null=True, blank=True, default="admin@gmail.com")
    uploaded = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)  
    
    def __str__(self):
        return self.title


class Review(models.Model):
    comment_by = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=False)
    created = datetime.datetime.now()
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
    country = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.country


class Fixture (models.Model):
    fixture = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.fixture


class News (models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    imageBy = models.CharField(max_length=200, default="Funolympics Admin")
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.title


class Standing (models.Model):
    country = models.CharField(max_length=200)
    gold = models.IntegerField()
    silver = models.IntegerField()
    bronze = models.IntegerField()
    total = models.IntegerField()

    def __str__(self):
        return self.country
