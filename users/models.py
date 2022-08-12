from django.utils import timezone

from time import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django_countries.fields import CountryField
# Create your models here.


class UserManager (BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("You must provide an email address")
        if not username:
            raise ValueError("You must provide a username")
        
        
        
        user = self.model(
            email=self.normalize_email(email),
            username = username, 
        )        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username, 
            password=password,
        )
        
        user.is_admin = True
        user.is_staff = True
        user.is_superuser= True
        user.is_active=True
        user.save(using=self._db)
        return user
        
        
class User (AbstractBaseUser):
    email       =models.EmailField(verbose_name="email", max_length=60, unique=True)    
    username    = models.CharField (max_length=50, unique=True)
    password    = models.CharField(max_length=128)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login  = models.DateTimeField(auto_now=True, verbose_name='last login')
    is_admin    = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=False)
    is_staff    = models.BooleanField(default=False)
    is_superuser= models.BooleanField(default=False)
    full_name   = models.CharField(verbose_name="Full Name", max_length=60, null=True)
    country     = CountryField(verbose_name="Country/Region of residence", blank_label="Select country", null=True, )
    # first_name = 
    #lastname
    #country
    #dob
    
    
    USERNAME_FIELD = 'email' #use this field to login to the account instead of username
    REQUIRED_FIELDS=['username']
    
    objects = UserManager()
    
    def __str__(self):
        return self.email #to show multiple fields,add + "," + self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True