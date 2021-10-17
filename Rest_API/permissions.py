from rest_framework import permissions
from rest_framework.permissions import BasePermission


class FilesPermissions(BasePermission):
    """IN PROGRESS"""
    edit_methods = "GET"
    # message = 'dupa'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.groups.filter(name='Mentor').exists():
                return True
            elif request.method in permissions.SAFE_METHODS:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        # if obj.users.all():
        #
        #     print(obj.users.all)

        if request.user.groups.filter(name='Mentor').exists():
            return True

        if request.user.groups.filter(name='Student').exists() and request.method not in self.edit_methods:
            return True

        return False