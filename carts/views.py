from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, CreateAPIView
from .models import Cart
from .serializers import CartSerializer, CartReturnSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from products.models import Product, CartProducts
from products.serializers import CartProductsSerializer

# Create your views here.


class CartView(ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartReturnSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart = Cart.objects.get(user_id=self.request.user.id)
        cart_products = CartProducts.objects.get(cart_id=cart.id, many=True)

        return cart_products


class CartDetailView(CreateAPIView):
    queryset = CartProducts.objects.all()
    serializer_class = CartProductsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        import ipdb

        ipdb.set_trace()
        cart = Cart.objects.create(amount=0)
        # cart = Cart.objects.get(user_id=self.request.user.id)
        product_id = self.kwargs.get("pk")
        product = get_object_or_404(Product, id=product_id)
        # product.cart.add(cart)
