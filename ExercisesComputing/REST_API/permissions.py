from rest_framework import permissions
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenVerifySerializer


class TokenVerify(permissions.BasePermission):

    def has_permission(self, request, view):
        header_token = request.META.get('HTTP_AUTHORIZATION', None)
        data = {'token': header_token}
        if not header_token:
            return False

        try:
            TokenVerifySerializer().validate(data)
            return True
        except TokenError:
            return False
