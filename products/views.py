from .models import Product
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer
from ..permissions import IsEmployee
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)


# retorna todos os produtos
class ProductView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# retorna um produto e adiciona um produto ao carrinho
class ProductDetailView(RetrieveAPIView, CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# retorna todos os produtos vendidos e cadastra um novo produto no site
class ProductSellerView(ListAPIView, CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEmployee]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# atualiza e deleta um produto
class ProductSellerDetailView(UpdateAPIView, DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEmployee]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
