from rest_framework import serializers
from .models import WishList
from products.models import Product, WishListProducts
from products.serializers import ProductSerializer


class WishListProductSerializer(serializers.ModelSerializer):
    wishlist_products = serializers.SerializerMethodField()

    def get_wishlist_products(self, obj):
        products = Product.objects.filter(wishlist=obj)
        serializer = ProductSerializer(products, many=True)
        return serializer.data

    class Meta:
        model = WishList

        fields = ("wishlist_products",)
        read_only_fields = ["wishlist_products"]
        depth = 1


class WishListPivotSerializer(serializers.ModelSerializer):
    product_data = serializers.SerializerMethodField()

    def get_product_data(self, obj):
        product = ProductSerializer(obj.product)
        return product.data

    class Meta:
        model = WishListProducts

        fields = ["id", "wishlist", "product_data"]
        read_only_fields = ["id", "wishlist", "product_data"]
