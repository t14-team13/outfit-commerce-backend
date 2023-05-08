from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = self.context["request"].user
        user_addresses = Address.objects.filter(user=user)
        if user_addresses.count() >= 5:
            raise serializers.ValidationError('The user has already reached the maximum number of registered addresses.')
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        validated_data = {}
        user = self.context["request"].user
        address_set = Address.objects.filter(user=user)
        for address in address_set:
            address.selected = False
            address.save()
        validated_data["selected"] = True
        return super().update(instance, validated_data)


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
            "selected"
        ]
