from django.contrib import admin
from reviews.models import ReviewComment, Review
# Register your models here.

admin.site.register(ReviewComment)
admin.site.register(Review)
