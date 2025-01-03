from django.db import models
from accounts.models import User


class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="部门名称")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                               verbose_name="上级部门")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = verbose_name


class Employee(models.Model):
    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")  # 修改这里
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True,verbose_name="所属部门")
    position = models.CharField(max_length=100, blank=True, null=True, verbose_name="职位")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="电话号码", unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True, verbose_name="性别")
    birthday = models.DateField(blank=True, null=True, verbose_name="生日")
    hire_date = models.DateField(blank=True, null=True, verbose_name="入职日期")
    employee_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="员工编号")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        department_str = str(self.department) if self.department else "无部门"
        position_str = self.position if self.position else "无职位"
        phone_number_str = self.phone_number if self.phone_number else "无电话"
        gender_str = self.get_gender_display() if self.gender else "无性别"
        birthday = self.birthday.strftime('%Y-%m-%d %H:%M:%S') if self.birthday else "未创建生日"
        hire_date =self.hire_date.strftime('%Y-%m-%d %H:%M:%S') if self.hire_date else "未创建入职时间"
        employee_number = self.employee_number if self.employee_number else "未分配员工编号"
        created_at_str = self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else "无创建时间"
        updated_at_str = self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else "无更新时间"
        return (f"{self.user.username}-{self.user.email} - {department_str} - {position_str} - "
                f"{phone_number_str} - {gender_str} - {created_at_str} - {updated_at_str}"
                f"{birthday}-{hire_date}-{employee_number}")

    class Meta:
        verbose_name = '员工'
        verbose_name_plural = verbose_name