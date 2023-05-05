from rest_framework import serializers
from .models import Product, CartProducts


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product

        fields = [
            "id",
            "name",
            "description",
            "price",
            "category",
            "stock",
            "user_id",
        ]

        extra_kwargs = {
            "user_id": {"read_only": True},
        }

    def update(self, instance: Product, validated_data: dict) -> Product:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class CartProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProducts

        fields = ["product_id", "cart_id"]

        extra_kwargs = {
            "product_id": {"read_only": True},
            "cart_id": {"read_only": True},
        }
