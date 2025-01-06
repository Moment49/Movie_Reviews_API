from django.db import models

# Create your models here.
class Movies(models.Model):
    name = models.CharField(max_length=100)

class Movie_Review(models.Model):
    ...