from django.urls import path
from . import views

urlpatterns = [
    path("seller/order/<int:id>", views.OrderDetailView.as_view()),
]