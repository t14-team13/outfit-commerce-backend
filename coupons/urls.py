from django.urls import path
from .views import CouponView, CouponCartView

urlpatterns = [
    # Admin/POST -> Gera um cupom de desconto
    path("coupons/", CouponView.as_view()),
    # Usuário autenticado/POST -> Usa o cupom <coupon_code> no carrinho
    path("coupons/<str:coupon_code>/cart/", CouponCartView.as_view()),
]
