from .models import Product
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer, ProductSoldSerializer
from permissions import IsEmployee
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from orders.models import ProductsOrder
from django_filters import rest_framework as filters


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    category = filters.CharFilter(field_name="category", lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ["name", "category"]


# retorna todos os produtos
class ProductView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter


# retorna um produto
class ProductDetailView(RetrieveAPIView):
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

    def perform_create(self, serializer: ProductSerializer) -> None:
        user = self.request.user
        serializer.save(user=user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductSoldSerializer

    # Aguardando as outras rotas para fazer os testes
    # def get_queryset(self):
    #     sold_products = []
    #     user = self.request.user
    #     order_products = ProductsOrder.objects.all()
    #     for item in order_products:
    #         if item.product.user_id == user.id:
    #             sold_products.append(item)

    #     return sold_products


# atualiza e deleta um produto
class ProductSellerDetailView(UpdateAPIView, DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEmployee]
