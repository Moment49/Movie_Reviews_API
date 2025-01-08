from django.urls import path
from rest_framework.routers import DefaultRouter
from reviews.views import MovieReviewView, MovieReviewByTitle, UserDetailView, UserDeleteView, UserUpdateView

router = DefaultRouter()

router.register(r'reviews', MovieReviewView, basename="reviews")

urlpatterns = [
    path('reviews/movies/', MovieReviewByTitle.as_view(), name="movie_review_by_title"),
    path('user/<str:username>/', UserDetailView.as_view(), name="user_detail_view"),
    path('user/<int:user_id>/delete/', UserDeleteView.as_view(), name="user_delete_view"),
    path('user/<int:pk>/update/', UserUpdateView.as_view(), name="user_update_view")
]+router.urls