from django.urls import path
from .views import OrderDetailView, OrderCreateView, OrderListView

urlpatterns = [
    # Usuário autenticado/GET -> Retorna uma lista dos pedidos que o usuário fez
    path("order/", OrderListView.as_view()),
    # Usuário autenticado/POST -> Finaliza a compra e gera o pedido
    path("cart/order/", OrderCreateView.as_view()),
    # Employee(owner) -> Atualiza o status do pedido <pk>
    path("seller/order/<int:pk>/", OrderDetailView.as_view()),
]
