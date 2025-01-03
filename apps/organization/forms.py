from django import forms
from organization.models import Employee, Department
from accounts.models import User
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        labels = {
            'username': '用户名',
            'email': '邮箱',
            'password': '密码',
        }
        widgets = {
            'password': forms.PasswordInput(),
        }
        help_texts = {
            'email': None,
            'password': None,
        }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['department', 'position', 'phone_number', 'gender', 'birthday', 'hire_date',
                  'employee_number']
        labels = {
            'department': '所属部门',
            'position': '职位',
            'phone_number': '电话号码',
            'gender': '性别',
            'birthday': '生日时间',
            'hire_date': '入职时间',
            'employee_number': '员工编号',
        }
        widgets = {
            'gender': forms.RadioSelect(choices=Employee.GENDER_CHOICES),
        }
