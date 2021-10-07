from django.contrib.auth.models import Permission
from rest_framework import permissions
from rest_framework.permissions import BasePermission


class MentorAllowAllStudentAllowPartial(BasePermission):
    edit_methods = ("PUT", "PATCH", "DELETE")
    message = 'dupa'

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

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.groups.filter(name='Mentor').exists():
            return True

        if request.user.groups.filter(name='Student').exists() and request.method not in self.edit_methods:
            return True

        return False
