
# Create your models here.
# backend/api/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from django.contrib.auth.models import User

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field is required')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

# class Match(models.Model):
#     user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1_matches')
#     user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2_matches')
#     matched_at = models.DateTimeField(auto_now_add=True)
#     is_active = models.BooleanField(default=True)

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

class Like(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    liker = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)
