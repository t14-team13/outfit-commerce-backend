from rest_framework import serializers
from .models import Coupon, CouponPivot
from rest_framework.exceptions import ValidationError
import random
import string


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ("id", "code", "discount", "amount", "user_id")

        read_only_fields = ["id", "code", "user_id"]

    def create(self, validated_data):
        validated_data["code"] = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=5)
        )
        return super().create(validated_data)


class CouponCartSerializer(serializers.ModelSerializer):
    coupon = serializers.SerializerMethodField()

    def get_coupon(self, obj):
        coupon = Coupon.objects.get(id=obj.coupon.id)
        coupon.amount = coupon.amount - 1
        coupon.save()
        return coupon.code

    class Meta:
        model = CouponPivot
        fields = ("id", "coupon", "cart")

        read_only_fields = ["id", "coupon", "cart"]


class CouponReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ("code", "discount")

        read_only_fields = ["code", "discount"]
