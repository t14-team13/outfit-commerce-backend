from django.urls import path
from .views import CouponView, CouponCartView

urlpatterns = [
    path("coupons/", CouponView.as_view()),
    path("coupons/<str:coupon_code>/cart/", CouponCartView.as_view()),
]
