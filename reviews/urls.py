from django.urls import path
from rest_framework.routers import DefaultRouter
from reviews.views import (MovieReviewView, MovieReviewByTitle, ReviewCommentCreateView,
UserDetailView, UserDeleteView, UserUpdateView, MostLikedReviewByMovie)

router = DefaultRouter()

router.register(r'reviews', MovieReviewView, basename="reviews")

urlpatterns = [
    path('reviews/movies/', MovieReviewByTitle.as_view(), name="movie_review_by_title"),
    path('user/<int:user_id>/', UserDetailView.as_view(), name="user_detail_view"),
    path('user/<int:user_id>/delete/', UserDeleteView.as_view(), name="user_delete_view"),
    path('user/<int:pk>/update/', UserUpdateView.as_view(), name="user_update_view"),
    path('reviews/movies/<str:movie_id>/most-likes/', MostLikedReviewByMovie.as_view(), name="most_likes"),
    path('reviews/<int:review_id>/comments/', ReviewCommentCreateView.as_view(), name="comments"),
]+router.urls