from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='admin').exists():
            return True
        return request.method in permissions.SAFE_METHODS