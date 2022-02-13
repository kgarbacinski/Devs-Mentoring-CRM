from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView


class TestView(APIView):
    def get(self, *args, **kwargs):
        return Response({"ok":'ok'})