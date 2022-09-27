from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django_countries.fields import CountryField
import uuid
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class UserManager (BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("You must provide an email address")

        email=self.normalize_email(email)
        user = self.model(email=email, **extra_fields)             
        user.set_password(password)
        user.save(using=self._db)
        return user
     
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        email=self.normalize_email(email)
        user = self.create_user(email, password, **extra_fields)        
        user.save(using=self._db)
        return user
        
        
class User (AbstractBaseUser):
    email       = models.EmailField(verbose_name="email", max_length=60, unique=True)    
    username    = models.CharField (max_length=50, unique=True)
    password    = models.CharField(max_length=128)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login  = models.DateTimeField(auto_now=True, verbose_name='last login')
    is_admin    = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    is_superuser=  models.BooleanField(default=False)
    is_pass_reset = models.BooleanField(default=False)
    phone_number = PhoneNumberField(null=True, verbose_name='Phone Number', blank=False, )
    full_name   =models.CharField(max_length=60, null=True)
    country     =CountryField(blank=False, null=True, verbose_name="Counrty/Area of resdence", blank_label="Select Country")
    id          =models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
   
    # first_name = 
    # lastname
    # country
    # dob
        
    USERNAME_FIELD = 'email' #use this field to login to the account instead of username
    REQUIRED_FIELDS=['username', 'full_name', 'country', 'phone_number']
    
    objects = UserManager()
    
    def __str__(self):
        return self.email #to show multiple fields,add + "," + self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    

class Profile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    country = CountryField(blank=True, null=True, verbose_name="Counrty/Area of resdence", blank_label="Select Country")
    profile_image = models.ImageField(null=True, blank=True, upload_to='images/profile_pics/', default='images/profile_pics/default.jpg')
    phone_number = PhoneNumberField(null=True, verbose_name='Phone Number', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    
    def __str__(self):
        return str(self.user.username) 

class ContactMail (models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    receiver = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='contact_mails')
    full_name = models.CharField(max_length=255, null=True, blank=False, verbose_name='Name')
    email = models.EmailField(max_length=200, null=True, blank=False)
    subject = models.CharField(max_length=200, null=True, blank=False)
    message = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    
    def __str__(self):
        return str ( self.subject) 
    
    class Meta:
        ordering = ['is_read', '-created']
        
class ContactReply(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    receiver = models.EmailField(null=True, blank=False, max_length=255, default=None)
    message = models.TextField(null=True, blank=False,)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)
    
    def __str__ (self):
        return str(self.receiver.username)
    
class Inbox (models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    receiver = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=False, blank=False, default='Reset Password')
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    
    def __str__(self):
        return str ( self.subject) 
    
    class Meta:
        ordering = ['is_read', '-created']
        
