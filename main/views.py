from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.response import Response

from .models import *
from .serializers import *

class MainPostViewSet(viewsets.ModelViewSet):
    queryset = MainPost.objects.all()
    serializer_class = MainPostSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data)
        