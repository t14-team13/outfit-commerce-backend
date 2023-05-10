from django.urls import path
from .views import UserView, UserDetailView, UserProfileView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    # Admin/GET -> Retorna todos os usuários
    # Any/POST -> Registra um novo usuário
    path("users/", UserView.as_view()),
    # Usuário autenticado/GET -> Retorna os dados do usuário
    path("users/profile/", UserProfileView.as_view()),
    # Admin/GET -> Retorna os dados do usuário <pk>
    path("users/<int:pk>/", UserDetailView.as_view()),
    # Any/POST -> Login
    path("users/login/", jwt_views.TokenObtainPairView.as_view()),
]
