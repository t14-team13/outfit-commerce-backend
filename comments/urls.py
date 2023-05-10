from django.urls import path
from .views import CommentCreateView

urlpatterns = [
    # Usuário autenticado/GET -> Retorna os comentários do produto <pk>
    # Usuário autenticado/POST -> Adiciona um comentário ao produto <pk>
    path("products/comment/<int:pk>/", CommentCreateView.as_view()),
]
