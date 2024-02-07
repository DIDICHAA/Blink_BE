from django.db import models

# Create your models here.
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    star = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    # user, pro 모델 정리 후 추가 예정
    # created_user = models.ForeignKey('users.user', on_delete=models.CASCADE, null=True)
    # reviewed_pro = models.ForeignKey('pro.pro', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.review_title