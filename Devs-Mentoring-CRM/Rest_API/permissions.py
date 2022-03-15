from rest_framework import permissions


# class MentorAllowAllStudentAllowPartial(permissions.BasePermission):
#     edit_methods = ("PUT", "PATCH", "DELETE")
#
#     def has_permission(self, request, view):
#         if request.user.is_authenticated:
#             if request.user.groups.filter(name='Mentor').exists():
#                 return True
#             elif request.method in permissions.SAFE_METHODS:
#                 return True
#         return False
#
#     def has_object_permission(self, request, view, obj):
#         if request.user.is_superuser:
#             return True
#
#         if request.method in permissions.SAFE_METHODS:
#             return True
#
#         if request.user.groups.filter(name='Mentor').exists():
#             return True
#
#         if request.user.groups.filter(name='Student').exists() and request.method not in self.edit_methods:
#             return True
#
#         return False


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


class FileAccessPermission(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        if request.user.is_authenticated:
            return request.user.groups.filter(name='Mentor').exists() or request.user.is_superuser



class ExerciseCodePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
