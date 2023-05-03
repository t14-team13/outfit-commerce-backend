from rest_framework import permissions
from .products.models import Product
from rest_framework.views import View


class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        return request.user.is_employee
