from rest_framework import serializers
from django.core.mail import send_mail

from .models import Order
from products.models import Product
from products.serializers import ProductSerializer

class ReturnOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "category"
        ]

class OrderSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Order

        fields = [
            "id",
            "status",
            "created_at",
            "updated_at",
            "products",
            "user"
        ]

        read_only_fields = ["user"]

    def get_products(self, obj):
        products = obj.products.all()
        serializer = ReturnOrderSerializer(products, many=True)
        return serializer.data


    @staticmethod
    def send_email(order):
        send_mail(
            "Order Status Updated",
            f"The status of your order {order.id} has been updated to {order.status}.",
            settings.EMAIL_HOST,
            [order.user.email],
            fail_silently=False,
    )
