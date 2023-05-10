from django.urls import path
from .views import WishView, WishDetailView, WishViewList


urlpatterns = [
    # Usuário autenticado/POST -> Cria uma wishlist pro usuário
    path("wishlist/", WishView.as_view()),
    # Usuário autenticado/GET -> Retorna os produtos da wishlist do usuário
    path("wishlist/products/", WishViewList.as_view()),
    # Usuário autenticado/POST -> Adiciona o produto <pk> a wishlist do usuário
    path("wishlist/products/<int:pk>/", WishDetailView.as_view()),
]
