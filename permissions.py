from rest_framework import permissions
# from .products.models import Product
from rest_framework.views import View
from users.models import User


class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        return request.user.is_employee
    
class IsAdminOrPostOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.method == "POST" or request.user.is_staff)

class IsAdminOrAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        return request.user.is_authenticated and obj == request.user or request.user.is_staff