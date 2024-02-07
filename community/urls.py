from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register(r'community/posts', PostViewSet, basename='community')
router.register(r'my-draft', MyDraftViewSet, basename='my-draft')

comments_router = routers.SimpleRouter()
comments_router.register(r'community/(?P<post_id>\d+)/comment', CommentViewSet, basename='post_comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(comments_router.urls)),
]