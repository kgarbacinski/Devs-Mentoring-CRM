from rest_framework import permissions
from rest_framework.permissions import BasePermission


class FilesPermissions(BasePermission):
    """IN PROGRESS"""
    edit_methods = "GET"

    def has_permission(self, request, view):
        if request.user.is_authenticated:
                return True
        return False

    def has_object_permission(self, request, view, obj):

        if request.user.is_superuser:
            return True

        if request.user.groups.filter(name='Mentor').exists():
            return True

        if obj.subtopic.user == request.user: ##TODO
            return True


        return False