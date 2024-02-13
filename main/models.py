from django.db import models

class MainPost(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now=True)
    start_date = models.CharField(max_length=20)
    end_date = models.CharField(max_length=20)
    address = models.TextField(max_length=200)
    latitude = models.CharField(max_length=10)
    longtitude = models.CharField(max_length=10)
    CATEGORY_CHOICES = [
        ('교통사고', '교통사고'),
        ('도난, 절도', '도난, 절도'),
        ('실종신고', '실종신고'),
        ('기타', '기타')
    ]
    ARTICLE_CHOICES= [
        ('찾아요', '찾아요'),
        ('제보해요', '제보해요')
    ]
    category = models.CharField(
        max_length=10,
        choices = CATEGORY_CHOICES,
        default = '교통사고',
    )
    article = models.CharField(
        max_length=10,
        choices = ARTICLE_CHOICES,
        default = '찾아요'
    )

class MainComment(models.Model):
    id = models.AutoField(primary_key=True)
    mainpost = models.ForeignKey(MainPost, blank=False, null=False, on_delete=models.CASCADE, related_name='comments')
    writer = models.CharField(max_length=50)
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now=True)

class MainReply(models.Model):
    id = models.AutoField(primary_key=True)
    maincomment = models.ForeignKey(MainComment, blank=False, null=False, on_delete=models.CASCADE, related_name='replies')
    writer = models.CharField(max_length=50)
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now=True)