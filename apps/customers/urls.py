from django.urls import path
from . import views
from customers.views import CustomerCreateView, customer_list

app_name = 'customers'
#
# urlpatterns = [
#     path('customer/add/', views.CustomerCreateView.as_view(), name='customer-add'),
#     path('customer/list/', views.customer_list, name='customer-list')
# ]

urlpatterns = [
    path('customer/list/', customer_list, name='customer-list'),
    path('customer/create/', CustomerCreateView.as_view(), name='customer-create'),
    # 其他相关的 URL 模式，例如更新和删除客户的 URL 模式
    path('customer/<int:pk>/update/', views.customer_update, name='customer-update'),
    path('customer/<int:pk>/delete/', views.customer_delete, name='customer-delete'),
    path('customer/<int:pk>/detail/', views.customer_detail, name='customer-detail'),
]

