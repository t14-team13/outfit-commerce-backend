from .models import Product
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer, ReturnSoldProductsSerializer
from permissions import IsEmployeeOrAdmin, ItsYoursOrAdmin
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from orders.models import ProductsOrder
from django_filters import rest_framework as filters
from orders.serializers import AnotherOrderSerializer


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    category = filters.CharFilter(field_name="category", lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ["name", "category"]


# retorna todos os produtos
class ProductView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ReturnSoldProductsSerializer
    filterset_class = ProductFilter


# retorna um produto
class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ListSelfProductsView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEmployeeOrAdmin]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = None

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)


# retorna todos os produtos vendidos e cadastra um novo produto no site
class ProductSellerView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEmployeeOrAdmin]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = None

    def perform_create(self, serializer: ProductSerializer) -> None:
        user = self.request.user
        serializer.save(user=user)

    # Pegar todos os produtos vendidos pelo usuário.


class ListSellerProductsView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEmployeeOrAdmin]
    queryset = ProductsOrder.objects.all()
    serializer_class = AnotherOrderSerializer
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        prods = ProductsOrder.objects.filter(product__user=user)
        return prods


# atualiza e deleta um produto
class ProductSellerDetailView(UpdateAPIView, DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, ItsYoursOrAdmin]
