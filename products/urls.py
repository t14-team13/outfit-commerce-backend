from django.urls import path
from . import views


urlpatterns = [
    path("products/"),
    path("products/<int:pk>"),
    path("seller/products/"),
    path("seller/products/<int:pk>"),
]
