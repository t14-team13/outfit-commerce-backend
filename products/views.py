from .models import Product
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer, ProductsSoldSerializer
from permissions import IsEmployee
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from orders.models import ProductsOrder, Order
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
class ProductSellerView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEmployee]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer: ProductSerializer) -> None:
        user = self.request.user
        serializer.save(user=user)


# atualiza e deleta um produto
class ProductSellerDetailView(UpdateAPIView, DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEmployee]


class ProductsSoldView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEmployee]
    queryset = ProductsOrder.objects.all()
    serializer_class = ProductsSoldSerializer

    def get_queryset(self):
        user = self.request.user
        order = Order.objects.filter(user=user)
        order_products = ProductsOrder.objects.filter(order=order)

        return order
