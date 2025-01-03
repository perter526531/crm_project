from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True, verbose_name="电话号码")
    email = models.EmailField(unique=True, verbose_name="邮箱")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
   # session_key = models.CharField(max_length=40, blank=True, null=True)  # 添加 session_key 字段
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = models.CharField(max_length=150, blank=True, null=True, unique=True, verbose_name="用户名")

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="accounts_user_groups",  # 添加 related_name
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="accounts_user_permissions",  # 添加 related_name
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
    #  constraints = [
    #   models.UniqueConstraint(fields=['email'], name='unique_email'),
    # ]


class UserSession(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=255)
    last_active = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Session for {self.user.email}"