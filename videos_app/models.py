from django.db import models
import uuid

# Create your models here.


class Video (models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    video=models.FileField(upload_to="videos/", null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    uploaded = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    
    

    def __str__(self):
        return self.title 


class Review(models.Model):

    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
 
class Tag (models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    
    def __str__(self):
        return self.name
    
    
class Fixture (models.Model):
    fixture = models.CharField(max_length=200)
    date    = models.CharField(max_length=200)
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
    gold    = models.IntegerField()
    silver  = models.IntegerField()
    bronze  = models.IntegerField()
    total   = models.IntegerField()
    
    def __str__(self):
        return self.country
    