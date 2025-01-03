# accounts/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User as AuthUser
from accounts.models import User


class AuthUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            # 尝试使用邮箱查找用户
            user = AuthUser.objects.get(email=username)
            if user.check_password(password):
                return user
        except AuthUser.DoesNotExist:
            # 尝试使用用户名查找用户
            try:
                user = AuthUser.objects.get(username=username)
                if user.check_password(password):
                    return user
            except AuthUser.DoesNotExist:
                return None


class AccountsBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)  # 从 accounts_user 表中通过 email 查找用户
            if user.check_password(password):  # 检查密码是否正确
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)  # 从 accounts_user 表中通过 user_id 获取用户
        except User.DoesNotExist:
            return None
