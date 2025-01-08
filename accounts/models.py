from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from rest_framework.validators import ValidationError

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name=None, last_name=None, username=None):
        if username is None:
            raise ValidationError("Username is required")
        if email is None:
            raise ValidationError("Email is required")
        if password is None:
            raise ValidationError('Password is required')
        
        user = self.model(email=self.normalize_email(email), username=username, first_name=first_name, last_name=last_name)
        user.set_password(password) #hashed password
        user.save(using=self._db) # save the using to db using the default database

        return user
    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True

        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

class UserProfile(models.Model):
    bio = models.TextField(max_length=200)
    profile_picture = models.ImageField(upload_to='uploads/', blank=True, null=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return f"{self.user.email}"
