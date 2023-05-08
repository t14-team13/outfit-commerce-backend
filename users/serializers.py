from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from addresses.models import Address
from addresses.serializers import AddressSerializer
from carts.serializers import CartProductsSerializer


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data: dict):
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
            else:
                setattr(instance, key, value)
        instance.save()
        return instance

    cart = CartProductsSerializer(read_only=True)
    address = serializers.SerializerMethodField(read_only=True)

    def get_address(self, obj):
        address_selected = Address.objects.filter(user=obj, selected=True)
        if not address_selected:
            return None
        return AddressSerializer(address_selected.first()).data

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_employee",
            "is_superuser",
            "address",
            "cart",
        ]

        extra_kwargs = {
            "password": {"write_only": True},
            "is_superuser": {"read_only": True},
            "username": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="A user with that username already exists.",
                    )
                ]
            },
            "email": {"validators": [UniqueValidator(queryset=User.objects.all())]},
        }
