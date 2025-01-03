# from django.shortcuts import render, redirect
# from django.views import View
# from django import forms
# from organization.models import Department, Employee
# from accounts.models import User
# from .forms import EmployeeForm, UserForm
# from django.core.exceptions import ValidationError
# import logging
#
# logger = logging.getLogger(__name__)
#
# class DepartmentForm(forms.ModelForm):
#    class Meta:
#        model = Department
#        fields = ['name','parent']
#
# class DepartmentCreateView(View):
#    def get(self, request):
#        from organization.models import Department # 修改这里
#        form = DepartmentForm()
#        return render(request, 'organization/department_form.html',{'form':form})
#
#    def post(self, request):
#        from organization.models import Department # 修改这里
#        form = DepartmentForm(request.POST)
#        if form.is_valid():
#            form.save()
#            return redirect('organization:department-list')  # 创建成功后重定向到部门列表页
#        else:
#            return render(request, 'organization/department_form.html',{'form':form})
#
#
# class EmployeeCreateView(View):
#    def get(self, request):
#        from organization.models import Department
#        employee_form = EmployeeForm()
#        user_form = UserForm()
#        return render(request, 'organization/employee_form.html', {'employee_form': employee_form, 'user_form': user_form})
#
#    def post(self, request):
#        from organization.models import Department, Employee
#        employee_form = EmployeeForm(request.POST)
#        user_form = UserForm(request.POST)
#        if employee_form.is_valid() and user_form.is_valid():
#            try:
#              user = user_form.save(commit=False)
#              user.username = f'employee_{user.email}'  # 设置 username 的值, 添加employee_前缀
#              user.set_password(user_form.cleaned_data['password'])
#              user.save()
#              employee = employee_form.save(commit=False)
#              employee.user = user
#              employee.save()
#              logger.info(f'成功创建用户： {user.email}')
#              return redirect('organization:employee-list')
#            except Exception as e:
#               user_form.add_error(None, f'创建用户失败, 错误信息: {e}')
#               logger.error(f'创建用户失败： {e}')
#               return render(request, 'organization/employee_form.html', {'employee_form': employee_form, 'user_form': user_form})
#        else:
#             logger.error(f'表单验证失败：{user_form.errors}')
#             return render(request, 'organization/employee_form.html', {'employee_form': employee_form, 'user_form': user_form})
#
# def department_list(request):
#     from organization.models import Department
#     departments = Department.objects.all()
#     return render(request, 'organization/department_list.html',{'departments':departments})
#
#
# def employee_list(request):
#    from organization.models import Employee
#    employees = Employee.objects.all()
#    return render(request, 'organization/employee_list.html', {'employees': employees})

from django.shortcuts import render, redirect
from django.views import View
from django import forms
from organization.models import Department, Employee
from accounts.models import User
from.forms import EmployeeForm, UserForm
from django.core.exceptions import ValidationError
import logging
from django.views.generic import UpdateView,DeleteView
from.models import Employee
from django.http import HttpResponseRedirect
from django.urls import reverse


logger = logging.getLogger(__name__)


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'parent']

class DepartmentCreateView(View):
    def get(self, request):
        form = DepartmentForm()
        departments = Department.objects.all()
        return render(request, 'organization/department_form.html', {'form': form, 'departments': departments})
    def post(self, request):
        form = DepartmentForm(request.POST)
        if form.is_valid():
            try:
                department = form.save()
                logger.info(f'成功保存部门：{department.name}')
                return redirect('organization:department-list')
            except Exception as e:
                import traceback
                traceback.print_exc()  # 打印完整的异常堆栈信息
                logger.error(f'保存部门时出错: {e}')
                form.add_error(None, '保存部门时出现错误，请重试。详细错误信息：' + str(e))
                return render(request, 'organization/department_form.html', {'form': form})
        else:
            logger.error(f'部门表单验证失败：{form.errors}')
            return render(request, 'organization/department_form.html', {'form': form})


class EmployeeCreateView(View):
    def get(self, request):
        employee_form = EmployeeForm()
        user_form = UserForm()
        return render(request, 'organization/employee_form.html', {'employee_form': employee_form, 'user_form': user_form})

    def post(self, request):
        employee_form = EmployeeForm(request.POST)
        print(employee_form)
        user_form = UserForm(request.POST)
        print(user_form)
        if employee_form.is_valid() and user_form.is_valid():
            try:
                user = user_form.save(commit=False)
                user.username = f'employee_{user.email}'
                user.set_password(user_form.cleaned_data['password'])
                user.save()
                employee = employee_form.save(commit=False)
                employee.user = user
                employee.save()
                department_id = request.POST.get('department')  # 假设你从表单中获取部门 ID
                if department_id:
                    employee.department = Department.objects.get(id=department_id)
                    print(f'employee.department:{employee.department}')
                employee.save()
                logger.info(f'成功创建用户： {user.email}')
                return redirect('organization:employee-list')
            except Exception as e:
                user_form.add_error(None, f'创建用户失败, 错误信息: {e}')
                logger.error(f'创建用户失败： {e}')
                return render(request, 'organization/employee_form.html', {'employee_form': employee_form, 'user_form': user_form})
        else:
            logger.error(f'表单验证失败：{user_form.errors}')
            return render(request, 'organization/employee_form.html', {'employee_form': employee_form, 'user_form': user_form})


def department_list(request):
    try:
        departments = Department.objects.all()
        return render(request, 'organization/department_list.html', {'departments': departments})
    except Exception as e:
        logger.error(f'获取部门列表时出错: {e}')
        return render(request, 'organization/department_list.html', {'departments': []})


def employee_list(request):
    try:
        employees = Employee.objects.select_related('user').all()
        return render(request, 'organization/employee_list.html', {'employees': employees})
    except Exception as e:
        import traceback
        traceback.print_exc()  # 打印完整的异常信息
        logger.error(f'获取员工列表时出错: {e}')
        return render(request, 'organization/employee_list.html', {'employees': []})

class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'organization/employee_update.html'
    success_url = '/organization/employee/list/'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        return render(request, self.template_name, {'form': form})


class DepartmentUpdateView(UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'organization/department_update.html'
    success_url = '/organization/department/list/'
    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(self.success_url)

class EmployeeDeleteView(DeleteView):
    model = Employee
    #template_name = 'organization/custom_employee_confirm_delete.html'  # 自定义模板名称
    success_url = '/organization/employee/list/'


class DepartmentDeleteView(DeleteView):
    model = Department
    success_url = '/organization/department/list/'