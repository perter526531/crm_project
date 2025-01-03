from django.db import models
from organization.models import Employee


class Customer(models.Model):
    STATUS_CHOICES = [
        ('normal', '正常'),
        ('shared', '共享池'),
    ]
    company_name = models.CharField(max_length=255, verbose_name="公司名称")
    website = models.URLField(blank=True, null=True, verbose_name="公司网站")
    legal_person = models.CharField(max_length=100, blank=True, null=True, verbose_name="法人")
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="负责员工")  # 外键指向  Employee  模型
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='normal', verbose_name="客户状态")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = '客户'
        verbose_name_plural = verbose_name


class Contact(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='contacts', verbose_name="客户")
    name = models.CharField(max_length=100, verbose_name="联系人姓名")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="联系人电话")
    position = models.CharField(max_length=100, blank=True, null=True, verbose_name="联系人职位")
    email = models.EmailField(blank=True, null=True, verbose_name="联系人邮箱")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="联系人地址")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = '联系人'
        verbose_name_plural = verbose_name