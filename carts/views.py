from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, CreateAPIView
from .models import Cart
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from products.models import Product, CartProducts
from .serializers import CartProductsSerializer, CartPivotSerializer
from rest_framework.exceptions import ValidationError


class CartView(ListAPIView, CreateAPIView):
    serializer_class = CartProductsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()
    pagination_class = None

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        cart_exist = Cart.objects.filter(user=self.request.user)
        if cart_exist:
            raise ValidationError({"error": "The user already contains a cart!"})
        return serializer.save(user=self.request.user)


class CartDetailView(CreateAPIView):
    queryset = CartProducts.objects.all()
    serializer_class = CartPivotSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart_exist, _ = Cart.objects.get_or_create(user=self.request.user)
        product_id = self.kwargs.get("pk")
        product = get_object_or_404(Product, id=product_id)
        serializer.save(cart=cart_exist, product=product)
