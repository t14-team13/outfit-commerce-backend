from django.urls import path
from .views import OrderDetailView, OrderCreateView, OrderListView

urlpatterns = [
    path("order/", OrderListView.as_view()),
    path("cart/order/", OrderCreateView.as_view()),
    path("seller/order/<int:pk>/", OrderDetailView.as_view()),
]