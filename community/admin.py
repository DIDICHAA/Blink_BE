from django.contrib import admin
from .models import Post, PostImage, Bookmark, Like, Comment

class PostImageInline(admin.TabularInline): # 인라인으로 이미지 편집
    model = PostImage

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline]
    list_display = ('title', 'content', 'created_at')
    list_filter = ('category',)  # 카테고리로 필터링

admin.site.register(Bookmark)
admin.site.register(Like)
admin.site.register(Comment)