from rest_framework import serializers
from .models import Cart
from products.models import CartProducts, Product
from rest_framework.validators import UniqueValidator


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ("id", "amount", "total_price", "user_id")
        extra_kwargs = {"id": {"read_only": True}, "user_id": {"read_only": True}}


# Mudar para o product serializer
class ProductReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "price")


class CartReturnSerializer(serializers.ModelSerializer):
    products_list = ProductReturnSerializer(many=True, read_only=True)

    class Meta:
        model = CartProducts
        fields = ("cart_id", "products_list")
        extra_kwargs = {
            "cart_id": {"read_only": True},
            "products_list": {"read_only": True},
        }
        # depth = 1

    def create(self, validated_data):
        return super().create(validated_data)
