from rest_framework import permissions
from rest_framework.views import View
from users.models import User


class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        return request.user.is_employee


class IsEmployeeOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        return request.user.is_employee or request.user.is_superuser


class IsAdminOrPostOnly(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        return bool(request.method == "POST" or request.user.is_staff)


class IsAdminOrAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        return bool(
            request.user.is_authenticated
            and obj == request.user
            or request.user.is_staff
        )


class itsYours(permissions.BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        return bool(request.user.is_authenticated and obj.user == request.user)


class ItsYoursOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated
            and obj.user == request.user
            or request.user.is_staff
        )
