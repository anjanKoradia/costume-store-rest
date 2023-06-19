from rest_framework import permissions


class IsVendor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == "vendor":
            return True

        return False
