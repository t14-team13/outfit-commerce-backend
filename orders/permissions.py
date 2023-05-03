from rest_framework import permissions
from rest_framework.views import Request, View
from users.models import User

class IsEmployeeAuthentication(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: User):
        return(
            request.user.is_authenticated
            and request.user.is_employee
        )