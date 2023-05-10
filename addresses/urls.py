from django.urls import path
from .views import AddressCreateView, AddressUpdateView

urlpatterns = [
    # Usuário autenticado/GET -> Listar todos meus endereços
    # Usuário autenticado/POST -> Criar um endereço (máximo 5)
    path("address/", AddressCreateView.as_view()),
    # Usuário autenticado(owner)-Admin/PATCH -> define o campo do endereço <pk> (selected) como 'true', e define os outros como 'false'
    # Admin/GET -> Lista os dados do endereço <pk>
    path("address/<int:pk>/", AddressUpdateView.as_view()),
]
