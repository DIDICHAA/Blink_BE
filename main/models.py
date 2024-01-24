from django.db import models

class Main(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now=True)
    CATEGORY_CHOICES = [
        ('교통사고', '교통사고'),
        ('도난, 절도', '도난, 절도'),
        ('실종신고', '실종신고'),
        ('기타', '기타')
    ]
    REPORT_CHOICES= [
        ('찾아요', '찾아요'),
        ('제보해요', '제보해요')
    ]
    category = models.CharField(
        max_length=10,
        choices = CATEGORY_CHOICES,
        default = '교통사고',
    )
    report = models.CharField(
        max_length=10,
        choices = REPORT_CHOICES,
        default = '찾아요'
    )