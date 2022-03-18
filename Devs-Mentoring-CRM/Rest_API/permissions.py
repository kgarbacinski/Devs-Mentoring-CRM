from rest_framework import permissions


class MentorCreate(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.groups.filter(name='Mentor').exists():
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Mentor').exists():
            return True
        return False


class MentorAccess(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        if request.user.is_authenticated and request.user.groups.filter(name='Mentor').exists():
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Mentor').exists():
            return True
        return False
        

class FileAccessPermission(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        if request.user.is_authenticated:
            return request.user.groups.filter(name='Mentor').exists() or request.user.is_superuser


class ExerciseCodePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
