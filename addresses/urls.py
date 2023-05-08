from django.urls import path
from .views import AddressCreateView, AddressUpdateView

urlpatterns = [
    path("address/", AddressCreateView.as_view()),
    path("address/<int:pk>/", AddressUpdateView.as_view()),
]
