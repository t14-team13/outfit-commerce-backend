from django.urls import path
from .views import AddressCreateView

urlpatterns = [
    path("address/", AddressCreateView.as_view()),
]
