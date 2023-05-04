from rest_framework import generics
from rest_framework_simplejwt.authenticarion import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Order
from .serializers import OrderSerializer
from ..permissions import IsEmployee


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
    permission_classes = [IsEmployee]
    
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        updated_instance = serializer.update(instance, request.data)

        if updated_instance.status != instance.status:
            serializer.send_email(updated_instance)

        return Response(serializer.data)
      