from django.http import Http404
from django.shortcuts import render
from rest_framework import generics

from Files_organizer.models import Document
from Rest_API.permissions import FilesPermissions
from Rest_API.serializers import DocumentSerializer


class DocumentView(generics.ListAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [FilesPermissions]

    def get_queryset(self):
        subtopic_id = self.kwargs['pk']
        query = Document.objects.filter(subtopic_id=subtopic_id).all()
        if not query:
            raise Http404
        return query

