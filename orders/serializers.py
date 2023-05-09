from rest_framework import serializers
from django.core.mail import send_mail

from .models import Order
from products.models import Product
from products.serializers import ProductSerializer


class ReturnOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "category"]

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
            "user",
        ]

        read_only_fields = ["user"]

    def get_products(self, obj):
        products = obj.products.all()
        serializer = ReturnOrderSerializer(products, many=True)
        return serializer.data

    def update_stock(self, product_id, stock):
        product = Product.objects.get(id=product_id)
        if product.stock == 0:
            raise serializers.ValidationError("Product not available")
        product.stock -= stock
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

class CreateOrderSerializer(serializers.ModelSerializer):
    cart_products = ProductSerializer(read_only=True, many=True)
    orders = OrderSerializer(
        read_only=True, many=True, source="orders"
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "orders"
            "cart_products"
        ]

        read_only_fields = ["user"]

    def create(self, validated_data):
        user = validated_data.pop("user")
        cart = user.cart

        cart_products = CartProducts.objects.filter(cart=cart).values_list(
            "product_id", flat=True
        )

        products = [
            Product.objects.get(id=product_id)
            for product in cart_products
        ]

        new_list = ProductSerializer(products, many=True)
        sellers = ser([
            product['user']
            for product in new_list.data
        ])

        new_orders = []

        for seller in sellers:
            order_products = []

            for product in new_list.data:
                if seller == product["user"]:
                    order_products.append(product)
            
            buyer = validated_data.copy()
            buyer["products"] = order_products

            order = Order.objects.create(**buyer, user=user)
            new_orders.append(order)
        
        cart.delete()

        return new_orders

    