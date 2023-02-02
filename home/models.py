from distutils.command.upload import upload
import email
from email.policy import default
from pyexpat import model
from tabnanny import verbose
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# Create your models here.

# class CustomUserManager(BaseUserManager):


# class User(AbstractBaseUser,PermissionsMixin):
#     email=models.EmailField(db_index=True, unique=True, max_length=254)
#     first_name=models.CharField(max_length=240
#     )
#     last_name=models.CharField(max_length=255
#     )
#     is_staff=models.BooleanField(default=True)
#     is_active=models.BooleanField(default=True)
#     is_superuser=models.BooleanField(default=False)

#     objects= CustomUserManager()

#     USERNAME_FIELD = 'User'
#     REQUIRED_FIELDS=['first_name','last_name']

#     class Meta:
#         verbose_name = 'User'
#         verbose_name_plural = 'Users'


class Userlogin(models.Model):
    # DESIGNATION = (
    #     ('Student', 'Student'),
    #     ('Faculty', 'Faculty'),
    #     ('Admin Officer', 'Admin officer'),
    #     ('Non Faculty Teacher', 'Non Faculty Teacher'),
    #     ('Admin', 'admin'),
    #     ('Helper', 'Helper')

    # )

    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    id = models.IntegerField(default=0)
    role = models.CharField(max_length=50)
    number = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='userImages', default='no image')
    image2 = models.ImageField(upload_to='userImages', default='no image')

    def __str__(self):
        return self.name

# class Userlogin(models.Model):

#     lodger = models.CharField(max_length=100)
#     accuser = models.IntegerField(default=0)
#     reason = models.IntegerField(default=0)
#     reviewer = models.CharField(max_length=50)
#     number = models.BigAutoField(primary_key=True)

#     def __str__(self):
#         return self.name


class Complains(models.Model):

    lodger = models.IntegerField(default=0)
    perpenetrer = models.CharField(max_length=250)
    reviewer = models.IntegerField(default=0)
    reason = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='complainImages', default='no image')
    status = models.CharField(max_length=50, default='Pending')
    comment = models.CharField(max_length=250, default=' ')

    def __str__(self):
        return self.reason
