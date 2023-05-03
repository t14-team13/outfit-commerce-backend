from rest_framework import serializers
from .models import Cart
from products.models import CartProducts, Product


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}, "user_id ": {"read_only": True}}


# Mudar para o product serializer
class ProductReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "price")


class CartReturnSerializer(serializers.ModelSerializer):
    products_list = ProductReturnSerializer(many=True)

    class Meta:
        model = CartProducts
        fields = ("cart_id", "products_list")
        extra_kwargs = {
            "cart_id": {"read_only": True},
            "products_list": {"read_only": True},
        }
        # depth = 1
