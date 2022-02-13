from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenVerifySerializer


class TokenCheck(MiddlewareMixin):

    def _init_(self, get_response):
        self.get_response = get_response

    def _call_(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        header_token = request.META.get('HTTP_AUTHORIZATION', None)
        data = {'token': header_token}
        if not header_token:
            return JsonResponse({'details': "Unauthorized:"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            TokenVerifySerializer().validate(data)
        except TokenError:
            return JsonResponse({'details': "Unauthorized:"}, status=status.HTTP_401_UNAUTHORIZED)
