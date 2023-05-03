from django.urls import path
from . import views


urlpatterns = [
    path("cart/products/", views.CartView.as_view()),
    path("cart/products/<int:pk>/", views.CartDetailView.as_view()),
]