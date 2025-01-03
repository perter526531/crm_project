from django.urls import path
from . import views



app_name = 'accounts' # 添加 app_name

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.index, name='index')  # 添加 index 的 url
]
