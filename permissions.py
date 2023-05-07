from rest_framework import permissions
from rest_framework.views import View, Request
from users.models import User
from products.models import Product


class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        return request.user.is_employee

class IsProductOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj):
        return obj.user == request.user

class IsAdminOrPostOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.method == "POST" or request.user.is_staff)


class IsAdminOrAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        return (
            request.user.is_authenticated
            and obj == request.user
            or request.user.is_staff
        )
