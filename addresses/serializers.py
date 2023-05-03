from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return super().create(validated_data)

    class Meta:
        model = Address
        fields = [
            "id",
            "street",
            "city",
            "state",
            "number",
            "complement",
            "zipcode",
        ]
