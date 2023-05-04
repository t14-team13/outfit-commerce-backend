from django.urls import path
from .views import OrderDetailView

urlpatterns = [
    path("seller/order/<int:id>/", OrderDetailView.as_view()),
]