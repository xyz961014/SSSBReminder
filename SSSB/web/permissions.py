from rest_framework import permissions

class ReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow read-only access.
    """

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
