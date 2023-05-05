from rest_framework import serializers
from django.core.mail import send_mail

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
            self.send_email(instance)

        return instance