
# Create your models here.
# backend/api/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
#上面這行是為了引入這三個類別是Django提供的用來自定義User模型的類別 
#AbstractBaseUser: 用來自定義User模型的基礎類別 
#BaseUserManager: 用來自定義User模型的管理器類別

from django.db import models

from django.contrib.auth.models import User

#Django ORM Object-Relational Mapping(models.CharField, models.ForeignKey, models.DateTimeField, models.BooleanField)
#
class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('The Username field is required')
        user = self.model(username=username)
        user.set_password(password)  # 將密碼進行哈希加密存儲
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)  # 唯一帳號
    password = models.CharField(max_length=128)  # 密碼欄位
    #is_online = models.BooleanField(default=False)  # 新增在線狀態
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()#自定義管理器!! 這樣才能使用自定義的create_user方法 #objects 不能改
   
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class Match(models.Model):
    user1 = models.ForeignKey(User, related_name='matches_as_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='matches_as_user2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


class Message(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

class Friendship(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1_friends')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2_friends')
    created_at = models.DateTimeField(auto_now_add=True)

# class Like(models.Model):
#     match = models.ForeignKey(Match, on_delete=models.CASCADE)
#     liker = models.ForeignKey(User, on_delete=models.CASCADE)
#     liked_at = models.DateTimeField(auto_now_add=True)
