from rest_framework import serializers
from products.models import CartProducts, Product
from products.models import Product
from products.serializers import ProductSerializer
from coupons.serializers import CouponReturnSerializer
from .models import Cart
from coupons.models import CouponPivot


class CartPivotSerializer(serializers.ModelSerializer):
    product_data = serializers.SerializerMethodField()

    def get_product_data(self, obj):
        product = ProductSerializer(obj.product)
        return product.data

    class Meta:
        model = CartProducts

        fields = ["id", "cart", "product_data"]
        read_only_fields = ["cart", "product_data"]


class CartProductsSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    # coupons = serializers.SerializerMethodField()
    coupons_used = CouponReturnSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def sum_amount_or_price(self, obj):
        user = self.context.get("request").user

        products = Product.objects.filter(cart=obj)
        coupon = CouponPivot.objects.filter(cart=obj)

        amount = 0
        price = 0
        discount = 0

        for i, value in enumerate(products):
            amount += 1
            price += value.price

        for coupon_pivot in coupon:
            discount += coupon_pivot.coupon.discount

        price = price - (price * discount / 100)

        return amount, price

    def get_products(self, obj):
        products = Product.objects.filter(cart=obj)

        serializer = ProductSerializer(products, many=True)
        return serializer.data

    def get_amount(self, obj):
        amount, _ = self.sum_amount_or_price(obj)

        return amount

    def get_total_price(self, obj):
        _, price = self.sum_amount_or_price(obj)

        return price

    class Meta:
        model = Cart

        fields = ("id", "products", "amount", "coupons_used", "total_price")
        read_only_fields = ["coupons_used"]

        depth = 1
