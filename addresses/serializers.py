from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        user = self.context["request"].user
        if user.address:
            raise serializers.ValidationError('The user already has an address.')
        return super().validate(attrs)

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
