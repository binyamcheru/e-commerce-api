
from rest_framework import permissions

class GuestPermission(permissions.BasePermission):
    """Allow read-only access to all users (authenticated and unauthenticated)."""
    def has_permission(self, request, view):
        # Allow GET, HEAD, OPTIONS requests for anyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Deny other methods for unauthenticated users
        return request.user and request.user.is_authenticated

class IsCustomer(permissions.BasePermission):
    """Allow access only to authenticated users with the 'customer' role."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'customer'

class IsAdmin(permissions.BasePermission):
    """Allow access only to authenticated users with the 'admin' role."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'

class IsSuperAdmin(permissions.BasePermission):
    """Allow access only to authenticated users with the 'superadmin' role."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'superadmin'

class IsAdminOrSuperAdmin(permissions.BasePermission):
    """Allow access only to authenticated users with 'admin' or 'superadmin' role."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.role == 'admin' or request.user.role == 'superadmin')

class IsOwner(permissions.BasePermission):
    """Allow access only to the owner of the review."""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user