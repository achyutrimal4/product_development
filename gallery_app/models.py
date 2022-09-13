from pickle import FALSE
from django.db import models
from users.models import Profile
from django.conf import settings
import uuid

# Create your models here.


class Photo (models.Model):
    description = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='images/gallery/', blank=FALSE)
    album = models.ForeignKey(
        'Album', verbose_name="Album", on_delete=models.SET_NULL, null=True)
    uploaded = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)  
    
    def __str__(self):
        return self.description
    
class Album(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name="Album")
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    
    def __str__(self):
        return self.name