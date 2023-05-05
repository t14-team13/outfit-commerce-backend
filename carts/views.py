from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, CreateAPIView
from .models import Cart
from .serializers import CartSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from products.models import Product, CartProducts
from products.serializers import CartProductsSerializer
from rest_framework.exceptions import ValidationError

# Create your views here.


class CartView(ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartDetailView(CreateAPIView):
    queryset = CartProducts.objects.all()
    serializer_class = CartProductsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart = Cart.objects.get(user_id=self.request.user.id)
        product_id = self.kwargs.get("pk")
        product = get_object_or_404(Product, id=product_id)
        serializer.save(cart=cart, product=product)


class CartCreateView(CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart_exist = Cart.objects.get(user=self.request.user)

        if not cart_exist:
            return serializer.save(user=self.request.user)

        raise ValidationError({"error": "User cart already exists"})
