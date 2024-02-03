from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    # 일반 user
    def create_user(self, email, nickname, isExpert, password):
        if not email:
            raise ValueError(('The Email must be set'))
        if not nickname:
            raise ValueError('must have user nickname')
        
        email = self.normalize_email(email)
        user = self.model(
            email = email,
            nickname = nickname,
            isExpert = isExpert,
        )
        user.set_password(password)
        user.save()
        return user

    # 슈퍼 user
    def create_superuser(self, email, nickname, isExpert, password):
        user = self.create_user(
            email,
            password = password,
            nickname = nickname,
            isExpert = isExpert,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractUser, PermissionsMixin):
    username = None
    id = models.AutoField(primary_key=True)
    email = models.EmailField(default='', max_length=255, null=False, blank=True, unique=True)
    nickname = models.CharField(default='', max_length=100, null=False, blank=False, unique=True)
    isExpert = models.BooleanField(default=False, blank=False, null=False)

    is_active = models.BooleanField(default=True)    
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['isExpert', 'nickname']

    objects = UserManager()

    def __str__(self):
        return self.email