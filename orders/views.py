from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Order, ProductsOrder
from products.models import CartProducts
from .serializers import OrderSerializer
from permissions import IsEmployee, ItsYoursOrAdmin
from rest_framework.validators import ValidationError


# Criar um pedido do carrinho do usuário
class OrderCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        user = self.request.user
        try:
            cart = user.cart
        except:
            raise ValidationError({"error": "user has no cart"})
        cart_products = CartProducts.objects.filter(cart=cart)
        if not len(cart_products):
            raise ValidationError({"error": "your cart is empty"})

        orders = []
        stock_update = {}

        seller_products = {}

        for cart_product in cart_products:
            product = cart_product.product
            seller_id = product.user_id

            try:
                seller_products[product.user] += [product]
            except KeyError:
                seller_products[product.user] = [product]

            if product.id not in stock_update:
                stock_update[product.id] = {"stock": 0, "sold": 0}
            stock_update[product.id]["stock"] += 1
            stock_update[product.id]["sold"] += 1

        for key, value in seller_products.items():
            order = Order.objects.create(user=key, cart=cart)

            for product in value:
                ProductsOrder.objects.create(
                    order=order,
                    product=product,
                )

        for product_id, update in stock_update.items():
            serializer.update_stock(product_id, update["stock"], update["sold"])

        user.cart.products_in_cart.set([])

        serializer.save(order=order)


# Lista os produtos do pedido
class OrderListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user

        return Order.objects.filter(user=user)


# Atualização do status do pedido
class OrderDetailView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployee, ItsYoursOrAdmin]

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def partial_update(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        status = request.data.get("status")
        if not status:
            raise ValidationError(
                {
                    "error": "status is a required field, choises are: Order placed, Order in progress and Order delivered"
                }
            )
        updated_order = serializer.update(order, {"status": status})

        if updated_order and order.status != status:
            serializer.send_mail(order)

        return Response(serializer.data)
