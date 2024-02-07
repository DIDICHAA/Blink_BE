from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register(r'community/posts', PostViewSet, basename='communities')
router.register(r'my-drafts', MyDraftViewSet, basename='my-drafts')
router.register(r'my-likes', MyLikePostViewSet, basename='my-likes')
router.register(r'my-bookmarks', MyBookmarkPostViewSet, basename='my-bookmarks')

comments_router = routers.SimpleRouter()
comments_router.register(r'community/(?P<post_id>\d+)/comment', CommentViewSet, basename='post_comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(comments_router.urls)),
    path('community/posts/<int:post_id>/like_status', get_post_like_status, name='get_like_status'),
    path('community/posts/<int:post_id>/bookmark_status', get_post_bookmark_status, name='get_bookmark_status'),
]