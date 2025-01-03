from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views import View
from django import forms
from django.contrib.auth.decorators import login_required
from accounts.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User as AuthUser
import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)


class LoginForm(forms.Form):
    email = forms.CharField(required=True, label="邮箱")
    password = forms.CharField(required=True, widget=forms.PasswordInput(), label="密码")


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)  # 使用 authenticate 验证 `auth_user`  表用户
            if user:
                logger.info(f"auth_user表使用邮箱登录成功， 邮箱：{user.email}, 用户名:{user.username}")
                login(request, user)  # 使用 login 函数记录信息
                return redirect('accounts:index')  # 跳转到首页

            user = User.objects.filter(email=email).first()  # 尝试使用邮箱查找 accounts_user 表
            if user:
                if check_password(password, user.password):  # 使用 `check_password` 验证密码
                    logger.info(f"accounts_user表使用邮箱登录成功， 邮箱：{user.email}, 用户名:{user.username}")
                    login(request, user,backend='accounts.backends.AccountsBackend')  # 使用 login 函数记录登录信息，并且需要使用自定义的 backend
                    return redirect('accounts:index')  # 登录成功后重定向到首页

            form.add_error(None, f'无效的邮箱或密码。 邮箱:{email}')
            logger.error(f"验证失败：无效的邮箱或密码。 邮箱:{email}")
            return render(request, 'accounts/login.html', {'form': form, 'next': request.GET.get('next')})
        else:
            form.add_error(None, f'表单验证错误')
            return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if request.user.is_authenticated:
        # 退出登录时，清除缓存中的会话数据
        session_key = f"user_session_{request.user.id}"
        cache.delete(session_key)  # 清除缓存中的会话
    logout(request)
    return redirect('accounts:login')


@login_required(login_url='accounts:login')
def index(request):
    return render(request, 'index.html')

