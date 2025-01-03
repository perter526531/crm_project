from django.urls import path
from . import views
from organization.views import DepartmentCreateView, EmployeeCreateView, department_list, employee_list

app_name = 'organization'

# urlpatterns = [
#     path('department/add/', views.DepartmentCreateView.as_view(), name='department-add'),
#     path('department/list/', views.department_list, name='department-list'),
#     path('employee/add/', views.EmployeeCreateView.as_view(), name='employee-add'),
#     path('employee/list/', views.employee_list, name='employee-list')
# ]
#
# urlpatterns = [
#     path('department/list/', department_list, name='department-list'),
#     path('department/add/', DepartmentCreateView.as_view(), name='department-add'),
#     path('employee/list/', employee_list, name='employee-list'),
#     path('employee/add/', EmployeeCreateView.as_view(), name='employee-add'),
#     # 确保这个 URL 模式存在
#     path('employee/update/<int:pk>/', views.EmployeeUpdateView.as_view(), name='employee-update'),
#     path('employee/delete/<int:pk>/', views.EmployeeDeleteView.as_view(), name='employee-delete'),
# ]

urlpatterns = [
    path('department/list/', department_list, name='department-list'),
    path('department/add/', DepartmentCreateView.as_view(), name='department-add'),
    path('employee/list/', employee_list, name='employee-list'),
    path('employee/add/', EmployeeCreateView.as_view(), name='employee-add'),
    path('employee/update/<int:pk>/', views.EmployeeUpdateView.as_view(), name='employee-update'),
    path('employee/delete/<int:pk>/', views.EmployeeDeleteView.as_view(), name='employee-delete'),
    # 添加以下部门更新的 URL 模式
    path('department/update/<int:pk>/', views.DepartmentUpdateView.as_view(), name='department-update'),
    path('department/delete/<int:pk>/', views.DepartmentDeleteView.as_view(), name='department-delete'),
]
