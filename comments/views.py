from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Comment
from .serializers import CommentSerializer
from products.models import Product
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination


class CommentsPagination(PageNumberPagination):
    page_size = 4


class CommentCreateView(CreateAPIView, ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CommentsPagination
    lookup_url_kwarg = "pk"

    def get_queryset(self):
        product_id = self.kwargs.get("pk")
        get_object_or_404(Product, id=product_id)
        return Comment.objects.all().filter(product_id=product_id)

    def perform_create(self, serializer) -> None:
        product_id = self.kwargs.get("pk")
        product = get_object_or_404(Product, id=product_id)
        user = self.request.user
        return serializer.save(product=product, user=user)
