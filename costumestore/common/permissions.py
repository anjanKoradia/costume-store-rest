from rest_framework import permissions


class IsVendor(permissions.BasePermission):
    """
        Permission class to allow access only to vendors.

        Methods:
            has_permission(request, view): Checks if the user has permission to access the view.
    """
    def has_permission(self, request, view):
        if request.user.role == "vendor":
            return True
        return False

class IsCustomer(permissions.BasePermission):
    """
        Permission class to allow access only to customers.

        Methods:
            has_permission(request, view): Checks if the user has permission to access the view.
    """
    def has_permission(self, request, view):
        if request.user.role == "customer":
            return True
        return False
