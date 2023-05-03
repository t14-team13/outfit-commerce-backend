from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer
from rest_framework import generics
from permissions import IsAdminOrPostOnly, IsAdminOrAccountOwner
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class UserView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrPostOnly]

    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        user_instance = self.get_object()
        new_pass = request.data.pop("password")
        if new_pass:
            user_instance.set_password(new_pass)
            user_instance.save()
        return super().update(request, *args, **kwargs)
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = "pk"

class UserProfileView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user_instance = self.get_object()
        new_pass = request.data.pop("password")
        if new_pass:
            user_instance.set_password(new_pass)
            user_instance.save()
        return super().update(request, *args, **kwargs)
    
    serializer_class = UserSerializer
    pagination_class = None

    def get_queryset(self):
        return User.objects.all().filter(id=self.request.user.id)
