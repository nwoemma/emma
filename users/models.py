from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    email = models.EmailField(('email address'), unique = True)
    phone_no = models.CharField(max_length = 11)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name','phone_no',]
    def __str__(self):
      return "{}".format(self.username)


