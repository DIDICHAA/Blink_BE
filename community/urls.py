from django.urls import path, include
from rest_framework import routers
from .views import *

app_name = 'community'

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'community', PostViewSet, basename='community')
router.register(r'my-draft', MyDraftViewSet, basename='my-draft')

urlpatterns = [
    path('', include(router.urls)),
]