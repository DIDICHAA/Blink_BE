from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.shortcuts import get_list_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .models import Post, PostImage, Comment
from .serializers import PostSerializer, CommentSerializer
from .paginations import *

# Create your views here.
class PostViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = PostSerializer
    pagination_class = PostPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']
    MAX_IMAGES = 3  # 클래스 변수로 상수 선언

    def get_queryset(self):
        return Post.objects.filter(is_draft=False).order_by('-created_at')
    
    def get_permissions(self):
        if self.action in ['list','retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

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


class MyDraftViewSet(PostViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Post.objects.filter(is_draft=True, writer=self.request.user).order_by('-created_at')

### Comment
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id') 
        if post_id is not None:
            return Comment.objects.filter(post__id=post_id, parent=None)  # post_id에 해당하는 원본 댓글만 가져오기
        return Comment.objects.filter(parent=None)  # 모든 댓글 가져오기
    
    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)