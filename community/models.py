from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def post_image_path(instance, filename):
    post = instance.post
    return f'post/{instance.category}/{post.id}/{post.created_at.strftime("%Y/%m/%d")}/{filename}'

# Create your models here.
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='제목',max_length=30,null=False,blank=False)
    writer = models.ForeignKey(User, on_delete=models.CASCADE) # 작성자가 계정 삭제시 게시글이 남아야한다면 변경 필요
    content = models.TextField(verbose_name='내용')
    CATEGORY_CHOICES = [
        ('몇대몇', '몇대몇'),
        ('영상 공유', '영상 공유'),
        ('자유', '자유'),
        ('질문', '질문'),
    ]
    category = models.CharField(verbose_name='카테고리', max_length=20, choices=CATEGORY_CHOICES)    
    created_at = models.DateTimeField(verbose_name='작성일', auto_now_add=True)

    def __str__(self):
        return self.title
    
        
    def images(self):
        return self.image.all()

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None, related_name='image')
    image = models.ImageField(upload_to=post_image_path)
    
    def __str__(self):
        return str(self.post)
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 좋아요 누른 사용자
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes') # 좋아요 누른 게시글

    class Meta:
        unique_together = ('user', 'post')  # 사용자는 같은 게시글에 중복 좋아요 불가능
    
    def __str__(self):
        return f"{self.user}가 좋아요한 글 : {self.post.title}"


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 북마크한 사용자
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='bookmarks') # 저장된 게시글

    class Meta:
        unique_together = ('user', 'post')  # 사용자는 같은 게시글에 중복하여 북마크 불가능
    
    def __str__(self):
        return f"{self.user}가 북마크한 글 : {self.post.title}"