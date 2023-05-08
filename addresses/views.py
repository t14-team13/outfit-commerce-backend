from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from permissions import IsAdminOrAccountOwner, itsYours
from addresses.serializers import AddressSerializer
from addresses.models import Address
from rest_framework.permissions import IsAuthenticated

class AddressCreateView(CreateAPIView, ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrAccountOwner]

    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    pagination_class = None

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
class AddressUpdateView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [itsYours]

    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    pagination_class = None
    lookup_url_kwarg = "pk"
    