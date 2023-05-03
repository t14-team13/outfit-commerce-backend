from rest_framework import serializers
from .models import Order
from carts.models import Cart
from products.models import Product

class OrderSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Order

        fields = [
            "id",
            "status",
            "created_at",
            "updated_at",
            "products"
        ]

    def get_user_cart_products(user):
        cart = Cart.objects.filter(user=user).first()
        if cart:
            return Product.objects.filter(cart=cart)
        else:
            return []

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        return instance