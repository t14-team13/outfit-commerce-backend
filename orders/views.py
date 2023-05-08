from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Order, ProductsOrder
from users.models import User
from products.models import CartProducts
from .serializers import OrderSerializer
from permissions import IsEmployee, IsProductOwner

#Criar um pedido de um carrinho existente
class OrderCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        user = self.request.user
        cart = user.cart
        cart_products = CartProducts.objects.filter(cart=cart)

        seller_products = {}
        for cart_product in cart_products:
            seller_id = cart_product.product.user_id
            if seller_id not in seller_products:
                seller_products[seller_id] = []
            seller_products[seller_id].append(cart_product.product)
        
        for seller_id, products in seller_products.items():
            seller_user = User.objects.get(id=seller_id)

            order = serializer.save(user=user, cart=cart)

            for product in products:
                ProductsOrder.objects.create(
                    order=order,
                    product=product,
                )
            
            order.user = seller_user
            order.save()

        cart_products.delete()

        # order = serializer.save(user=user, cart=cart)

        # for cart_product in cart_products:
        #     ProductsOrder.objects.create(
        #         order=order,
        #         product=cart_product.product,
        #     )

        # cart_products.delete()


#Lista os produtos do pedido
class OrderListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user

        return Order.objects.filter(user=user)

#Atualização do status do pedido
class OrderDetailView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployee, IsProductOwner]
    
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        updated_instance = serializer.update(instance, request.data)

        if updated_instance.status != instance.status:
            serializer.send_mail(updated_instance)

        return Response(serializer.data)
      