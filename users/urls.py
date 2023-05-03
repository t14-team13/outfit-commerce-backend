from django.urls import path
from .views import UserView, UserDetailView, UserProfileView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("users/", UserView.as_view()),
    path("users/profile/", UserProfileView.as_view()),
    path("users/<int:pk>/", UserDetailView.as_view()),
    path("users/login/", jwt_views.TokenObtainPairView.as_view()),
]
