from rest_framework import serializers
from django.core.mail import send_mail

from .models import Order
from products.serializers import ProductSerializer

class OrderSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    order = serializers.SerializerMethodField()

    class Meta:
        model = Order

        fields = [
            "id",
            "status",
            "created_at",
            "updated_at",
            "products",
            "order",
        ]

    def get_products(self, obj):
        products = obj.products.all()
        serializer = ProductSerializer(products, many=True)
        return serializer.data

    def get_order(self, obj):
        if "order" in self.context:
            order_serializer = OrderDetailSerializer(
                instance = self.context["order"]
            )
            return order_serializer.data

    @staticmethod
    def send_email(order):
        send_mail(
            "Order Status Updated",
            f"The status of your order {order.id} has been updated to {order.status}.",
            settings.EMAIL_HOST,
            [order.user.email],
            fail_silently=False,
    )

    def update(self, instance, validated_data):
        user = self.request.user

        status = validated_data.get('status')
        if status and status != instance.status:
            instance.status = status
            instance.save()
            self.send_email(instance, request=None)

        return instance