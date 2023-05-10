from rest_framework.generics import CreateAPIView, ListAPIView
from .models import WishList
from .serializers import WishListProductSerializer, WishListPivotSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from products.models import WishListProducts
from products.models import Product
from django.shortcuts import get_object_or_404


class WishViewList(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = WishListProductSerializer
    pagination_class = None

    def get_queryset(self):
        return WishList.objects.filter(user=self.request.user)


class WishView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = WishList
    serializer_class = WishListProductSerializer

    def perform_create(self, serializer):
        wishlist_exist = WishList.objects.filter(user=self.request.user)

        if wishlist_exist:
            raise ValidationError({"error": "The user already contains a WishList!"})

        return serializer.save(user=self.request.user)


class WishDetailView(CreateAPIView):
    queryset = WishListProducts.objects.all()
    serializer_class = WishListPivotSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.kwargs.get("pk")
        product = get_object_or_404(Product, id=product_id)
        wishlist_exist, _ = WishList.objects.get_or_create(user=self.request.user)
        wish_pivot =  WishListProducts.objects.filter(wishlist=wishlist_exist, product=product)
        
        if wish_pivot:
            raise ValidationError({"error": "product already exists in wishlist"})

        serializer.save(product=product, wishlist=wishlist_exist)
