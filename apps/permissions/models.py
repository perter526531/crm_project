from django.db import models

class Permission(models.Model):
   name = models.CharField(max_length=100, unique=True, verbose_name="权限名称")
   description = models.TextField(blank=True, null=True, verbose_name="权限描述")
   created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
   updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

   def __str__(self):
       return self.name
   class Meta:
       verbose_name = '权限'
       verbose_name_plural = verbose_name

class EmployeePermission(models.Model):
   employee = models.ForeignKey('organization.employee', on_delete=models.CASCADE, verbose_name="员工")
   permission = models.ForeignKey(Permission, on_delete=models.CASCADE, verbose_name="权限")
   created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
   updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

   class Meta:
       unique_together = ('employee', 'permission')
       verbose_name = '员工权限'
       verbose_name_plural = verbose_name