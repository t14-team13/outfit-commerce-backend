from rest_framework import serializers
from django.core.mail import send_mail
from .models import Order
from products.models import Product
from products.serializers import ProductSerializer
from .models import ProductsOrder


class ReturnOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "category", "user"]

class OrderSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Order

        fields = [
            "id",
            "status",
            "user",
            "created_at",
            "updated_at",
            "products",
        ]
        read_only_fields = ["user"]

    def get_products(self, obj):
        products = obj.products
        serializer = ReturnOrderSerializer(products, many=True)
        return serializer.data

    def create(self, validated_data):
        return validated_data["order"]

    def update_stock(self, product_id, stock, sold):
        product = Product.objects.get(id=product_id)
        if product.stock <= 0:
            raise serializers.ValidationError("Product not available")
        product.stock -= stock
        product.sold += sold
        product.available = product.stock > 0
        product.save()

        return product

    @staticmethod
    def send_email(order):
        send_mail(
            "Order Status Updated",
            f"The status of your order {order.id} has been updated to {order.status}.",
            settings.EMAIL_HOST,
            [order.user.email],
            fail_silently=False,
        )


class AnotherOrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductsOrder
        fields = ["id", "order", "product"]
        read_only_fields = ["id", "product", "order"]
