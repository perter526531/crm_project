from django.conf.global_settings import SESSION_COOKIE_AGE
from django.utils import timezone
from django.shortcuts import redirect
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.contrib.auth import logout




class SessionIdleTimeoutMiddleware:
     def __init__(self, get_response):
         self.get_response = get_response

     def __call__(self, request):
        if request.user.is_authenticated:
           session_idle_timeout = getattr(settings, 'SESSION_IDLE_TIMEOUT', None)
           if session_idle_timeout:
             last_activity = request.session.get('last_activity')
             if last_activity:
                 now = timezone.now()
                 time_since_last_activity = (now - timezone.datetime.fromisoformat(last_activity)).total_seconds()
                 if time_since_last_activity > session_idle_timeout:
                     from django.contrib.auth import logout
                     logout(request)
                     request.session.flush()
                     return redirect('accounts:login')
           request.session['last_activity'] = timezone.now().isoformat()
        response = self.get_response(request)
        return response


from django.core.cache import cache
from django.contrib.auth import logout
from django.shortcuts import redirect

class SingleSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # 使用用户ID作为会话的唯一标识
            session_key = f"user_session_{request.user.id}"

            # 获取当前缓存中的会话ID
            cached_session_key = cache.get(session_key)

            # 如果缓存中已有会话ID，并且与当前会话ID不一致，说明该用户在其他地方已登录
            if cached_session_key:
                if cached_session_key != request.session.session_key:
                    # 注销当前用户并删除会话数据
                    logout(request)
                    request.session.flush()
                    cache.delete(session_key)  # 清除缓存中的旧会话
                    return redirect('accounts:login')

            # 设置缓存，记录当前会话ID，并设置会话过期时间
            cache.set(session_key, request.session.session_key, timeout=SESSION_COOKIE_AGE)

        response = self.get_response(request)
        return response



