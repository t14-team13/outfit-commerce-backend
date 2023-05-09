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

#Criar um pedido do carrinho do usuário
class OrderCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        user = self.request.user
        cart = user.cart
        cart_products = CartProducts.objects.filter(cart=cart)

        orders = []
        stock_update = {}

        for cart_product in cart_products:
            product = cart_product.product
            seller_id = product.user_id

            order = serializer.save(user=user, cart=cart)
            order.save()
            orders.append(order)

            ProductsOrder.objects.create(
                order=order,
                product=product,
            )
        
            if product.id not in stock_update:
                stock_update[product.id] = 0
            stock_update[product.id] +=1

        for order in orders:
            order.save()

        for product_id, products_stock in stock_update.items():
            serializer.update_stock(product_id, products_stock)

        cart_products.delete()

        return OrderSerializer(orders, many=True).data


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

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def partial_update(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        status = request.data.get('status')
        updated_order = serializer.update(
            order,
            {"status": request.data['status']}
            )

        if updated_order and order.status != status:
            serializer.send_mail(order)

        return Response(serializer.data)


      