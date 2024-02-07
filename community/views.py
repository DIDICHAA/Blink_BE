from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.decorators import api_view, permission_classes

from drf_yasg.utils import swagger_auto_schema

from django.shortcuts import get_list_or_404, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from .models import Post, PostImage, PostLike, PostBookmark, Comment, CommentLike
from .serializers import PostSerializer, CommentSerializer
from .paginations import *

# Create your views here.
class PostBasicViewSet(viewsets.GenericViewSet,mixins.DestroyModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin):
    serializer_class = PostSerializer
    pagination_class = PostPagination
    MAX_IMAGES = 3  # 클래스 변수로 상수 선언

    def update(self, request, *args, **kwargs):
        image_set = request.FILES.getlist('images')

        if len(image_set) > self.MAX_IMAGES:
            response = {'error': f'최대 {self.MAX_IMAGES}개의 이미지를 업로드할 수 있습니다.'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()
        
        for image in instance.image.all():
            image.image.delete(save=False)  # 파일 삭제
            image.delete()  # 모델 인스턴스 삭제

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        for image_data in image_set:
            PostImage.objects.create(post=instance, image=image_data)

        return Response(serializer.data, status=status.HTTP_200_OK)

class PostViewSet(PostBasicViewSet, mixins.CreateModelMixin):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']
    
    def create(self, request, *args, **kwargs):
        image_set = request.FILES.getlist('images')

        if len(image_set) > self.MAX_IMAGES:
            response = {'error': f'최대 {self.MAX_IMAGES}개의 파일을 업로드 할 수 있습니다.'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        data_copy = request.data.copy()
        serializer = self.get_serializer(data=data_copy)
        serializer.is_valid(raise_exception=True)

        # perform_create 메서드에서 writer 필드를 설정
        self.perform_create(serializer, writer=request.user)

        instance = serializer.instance
        for image_data in image_set:
            PostImage.objects.create(post=instance, image=image_data)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer, writer):
        # save 메서드에 writer를 전달
        serializer.save(writer=writer)

    def get_queryset(self):
        return Post.objects.filter(is_draft=False).order_by('-created_at').annotate(
            likes_cnt=Count('likes',distinct=True)
        )

    def get_permissions(self):
        if self.action in ['list','retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(methods=['POST', 'DELETE'], detail=True, url_path='like')
    def like_action(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user
        post_like, created = PostLike.objects.get_or_create(post=post, user=user)

        if request.method == 'POST':
            post_like.save()
            message = '좋아요를 눌렀습니다.'
        
        elif request.method == 'DELETE':
            post_like.delete()
            message = '좋아요를 취소했습니다.'
        return Response({'message': message})

    @action(methods=['POST', 'DELETE'], detail=True, url_path='bookmark')
    def bookmark_action(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user
        post_bookmark, created = PostBookmark.objects.get_or_create(post=post, user=user)

        if request.method == 'POST':
            post_bookmark.save()
            message = '북마크에 저장했습니다.'
        
        elif request.method == 'DELETE':
            post_bookmark.delete()
            message = '북마크를 삭제했습니다.'
        
        return Response({'message': message})


class MyDraftViewSet(PostBasicViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(is_draft=True, writer=self.request.user).order_by('-created_at')

class MyBookmarkPostViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    
    def get_queryset(self):
        return Post.objects.filter(likes__user=self.request.user).order_by('-created_at').annotate(
            likes_cnt=Count('likes',distinct=True)
        )

class MyLikePostViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    pagination_class = PostPagination

    def get_queryset(self):
        return Post.objects.filter(bookmarks__user=self.request.user).order_by('-created_at').annotate(
            likes_cnt=Count('likes',distinct=True)            
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_post_like_status(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    is_liked = post.likes.filter(user=user).exists()
    return Response({'is_liked': is_liked})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_post_bookmark_status(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    is_bookmarked = post.bookmarks.filter(user=user).exists()
    return Response({'is_bookmarked': is_bookmarked})

### Comment
class CommentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins. CreateModelMixin, mixins.DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PostPagination

    def get_queryset(self):
        post_id = self.kwargs.get('post_id') 
        if post_id is not None:
            return Comment.objects.filter(post__id=post_id, parent=None).annotate(
                likes_cnt=Count('likes',distinct=True)
            )  # post_id에 해당하는 원본 댓글만 가져오기
        return Comment.objects.filter(parent=None).annotate(
                likes_cnt=Count('likes',distinct=True)
            )  # 모든 댓글 가져오기
    
    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    @action(methods=['POST', 'DELETE'], detail=True, url_path='like')
    def like_action(self, request, *args, **kwargs):
        comment = self.get_object()
        user = request.user
        comment_like, created = CommentLike.objects.get_or_create(comment=comment, user=user)

        if request.method == 'POST':
            comment_like.save()
            message = '좋아요를 눌렀습니다.'
        
        elif request.method == 'DELETE':
            comment_like.delete()
            message = '좋아요가 삭제되었습니다.'
        return Response({'message': message})