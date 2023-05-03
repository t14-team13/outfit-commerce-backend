from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.authenticarion import JWTAuthentication
from .serializers import OrderSerializer
from .permissions import IsEmployeeAuthentication
from django.shortcuts import get_object_or_404

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeeAuthentication]
    
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def perform_update(self, serializer):

        get_object_or_404()