from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    def create_user():
        ...
    def create_superuser():
        ...

class CustomUser(AbstractUser):
    ...

class UserProfile(models.Model):
    ...
