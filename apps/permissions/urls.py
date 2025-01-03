from django.urls import path
from . import views
app_name = 'permissions'
urlpatterns = [
    path('permission/list/', views.PermissionListView.as_view(), name='permission-list')
  ]