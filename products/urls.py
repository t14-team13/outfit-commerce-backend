from django.urls import path
from products.views import (
    ProductDetailView,
    ProductView,
    ProductSellerView,
    ProductSellerDetailView,
    ListSelfProductsView,
    ListSellerProductsView,
)


urlpatterns = [
    # Any/GET -> Retorna todos os produtos (filtro ?name= / ?category=)
    path("products/", ProductView.as_view()),
    # Employee-Admin/GET -> Retorna todos os produtos do usuário
    path("products/my/", ListSelfProductsView.as_view()),
    # Any/GET -> Retorna o produto <pk>
    path("products/<int:pk>/", ProductDetailView.as_view()),
    # Employee-Admin/POST -> Cadastra um novo produto
    path("seller/products/", ProductSellerView.as_view()),
    # Employee-Admin/GET -> Retorna os produtos cadastrados pelo usuário
    path("seller/products/my/", ListSellerProductsView.as_view()),
    # Employee(owner)-Admin/PATCH/DELETE -> Atualiza/Delete o produto <pk>
    path("seller/products/<int:pk>/", ProductSellerDetailView.as_view()),
]
