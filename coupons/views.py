from rest_framework.generics import CreateAPIView
from .models import Coupon, CouponPivot
from .serializers import CouponSerializer, CouponCartSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError


class CouponView(CreateAPIView):
    queryset = Coupon
    serializer_class = CouponSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CouponCartView(CreateAPIView):
    queryset = CouponPivot
    serializer_class = CouponCartSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            cart_user = self.request.user.cart

        except:
            raise ValidationError({"error": "user has no cart"})

        coupon_used_for_user = CouponPivot.objects.filter(cart=cart_user)

        coupon_code = self.kwargs.get("coupon_code")
        coupon = get_object_or_404(Coupon, code=coupon_code)

        if not coupon.amount:
            raise ValidationError({"error": "This coupon is expired!"})

        if coupon_used_for_user:
            raise ValidationError({"error": "You can only use one coupon per cart!"})

        serializer.save(coupon=coupon, cart=self.request.user.cart)
