from rest_framework import permissions


class FileAccessPermission(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        if request.user.is_authenticated:
            return request.user.groups.filter(name='Mentor').exists() or request.user.is_superuser
