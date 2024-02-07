from rest_framework.pagination import PageNumberPagination

class PostPagination(PageNumberPagination):
    page_size = 10

class PostCurtPagination(PageNumberPagination):
    page_size = 5