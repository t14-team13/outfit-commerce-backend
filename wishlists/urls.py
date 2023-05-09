from django.urls import path
from .views import WishView, WishDetailView, WishViewList


urlpatterns = [
    path("wishlist/", WishView.as_view()),
    path("wishlist/products/", WishViewList.as_view()),
    path("wishlist/<int:pk>/products/", WishDetailView.as_view()),
]
