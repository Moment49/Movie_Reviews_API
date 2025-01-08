from django.db import models
from django.contrib.auth import get_user_model

# Get the current User model that is active
CustomUser = get_user_model()


# Create your models here.
class Movies(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title}"

class Review(models.Model):
    MOVIE_RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    movie_title = models.ForeignKey(Movies, on_delete=models.CASCADE, related_name="reviews")
    content = models.TextField(max_length=200)
    rating = models.IntegerField(choices=MOVIE_RATING_CHOICES, blank=False, null=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content}"