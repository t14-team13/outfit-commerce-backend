from django.urls import path
from products.views import ProductDetailView, ProductView, ProductSellerView, ProductSellerDetailView


urlpatterns = [
    path("products/", ProductView.as_view()),
    path("products/<int:pk>/", ProductDetailView.as_view()),
    path("seller/products/", ProductSellerView.as_view()),
    path("seller/products/<int:pk>/", ProductSellerDetailView.as_view()),
]
