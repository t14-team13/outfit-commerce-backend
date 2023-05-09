from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    available = serializers.SerializerMethodField()

    def get_available(self, obj):
        if obj.stock > 0:
            return True
        return False

    class Meta:
        model = Product

        fields = [
            "id",
            "name",
            "image",
            "description",
            "price",
            "category",
            "stock",
            "user_id",
            "available",
        ]

        extra_kwargs = {
            "user_id": {"read_only": True},
            "available": {"read_only": True},
        }

    def update(self, instance: Product, validated_data: dict) -> Product:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
