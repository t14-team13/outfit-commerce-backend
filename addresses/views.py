from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import CreateAPIView
from permissions import IsAdminOrAccountOwner
from addresses.serializers import AddressSerializer
from addresses.models import Address

class AddressCreateView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrAccountOwner]

    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def perform_create(self, serializer) -> None:
        address = serializer.save()
        self.request.user.address = address
        self.request.user.save()
    