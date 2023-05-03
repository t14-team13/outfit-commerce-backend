from django.urls import path
from . import views


urlpatterns = [
    path("products/", views.ProductView.as_view()),
    path("products/<int:pk>/", views.ProductDetailView.as_view()),
    path("seller/products/", views.ProductSellerView.as_view()),
    path("seller/products/<int:pk>/", views.ProductSellerDetailView.as_view()),
]
