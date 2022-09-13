from django.core.mail import send_mail
from django.db.models.signals import post_save, post_delete
from .models import Profile, User
from django.dispatch import receiver