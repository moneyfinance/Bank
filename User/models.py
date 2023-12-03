from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.

# class User(AbstractUser):
#     phone_number = models.CharField(max_length=10,unique=True)
#     is_phone_verified = models.BooleanField(default=False)

#     USERNAME_FIELD = 'phone_number'
#     REQUIRED_FIELDS = []
#     objects = UserManager()

class User(AbstractUser):
    phone_number = models.CharField(max_length=10, unique=True)
    is_phone_verified = models.BooleanField(default=False)

    objects = UserManager()

    # Specify unique related_name values for groups and user_permissions
    groups = models.ManyToManyField(Group, related_name='user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='user_permissions', blank=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number

class Otp(models.Model):
    phone_number = models.CharField(max_length=10,unique=True)
    otp = models.CharField(max_length=4)
    created_at = models.TimeField( auto_now_add=True)       
    class Meta:
        db_table = 'pp_otp' 
