from django.urls import path
from . import views


urlpatterns = [
    # Usuário autenticado/POST -> Criar um carrinho
    # Usuário autenticado/GET -> Ver os produtos do carrinho
    path("cart/", views.CartView.as_view()),
    # Usuário autenticado/POST -> Adicionar o produto <pk> ao carrinho
    path("cart/<int:pk>/", views.CartDetailView.as_view()),
]
