from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('auth/register/', views.ResgisterView.as_view(), name="register"),
    path('auth/login/', views.login_view, name="login"),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair')
]