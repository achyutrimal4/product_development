from django.core.mail import send_mail
from django.db.models.signals import post_save, post_delete
from .models import Profile, User
from django.dispatch import receiver


@receiver(post_save, sender=Profile)
def updateProfile(sender, instance, created, **kwargs):
    print("Profile updated")
    print('Instance', instance)
    
    # post_save.connect(profile_updated, sender=Profile)
    
@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user, 
            username = user.username, 
            email = user.email,
            name = user.full_name,
            country = user.country,
        )
        

@receiver(post_save, sender=Profile)
def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created==False:
        user.full_name = profile.name
        user.username = profile.username
        user.country = profile.country
        user.save()
        

@receiver(post_delete, sender=Profile)    
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()
    

    
