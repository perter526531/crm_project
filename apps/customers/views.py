from django.shortcuts import render,redirect
from django.views import View
from django import forms
from customers.models import Customer, Contact
from django.db.models import Q
from django.core.exceptions import ValidationError
import logging


logger = logging.getLogger(__name__)


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['company_name', 'website', 'legal_person']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'phone_number', 'position', 'email', 'address']

class CustomerCreateView(View):
    def get(self, request):
        # 处理 GET 请求的逻辑，例如返回一个表单页面
        customer_form = CustomerForm()
        contact_form = ContactForm()
        return render(request, 'customers/customer_form.html', {'customer_form': customer_form, 'contact_form': contact_form})

    def post(self, request):
        # 处理 POST 请求的逻辑，例如创建新的客户
        customer_form = CustomerForm(request.POST)
        contact_form = ContactForm(request.POST)
        if customer_form.is_valid() and contact_form.is_valid():
            try:
                company_name = customer_form.cleaned_data['company_name']
                website = customer_form.cleaned_data['website']
                if Customer.objects.filter(Q(company_name=company_name) | Q(website=website)).exists():
                    customer = Customer.objects.filter(Q(company_name=company_name) | Q(website=website)).first()
                    employee = customer.employee
                    customer_form.add_error(None, f'公司名称或网站已存在，该客户所属员工为：{employee.user.username if employee else "该客户未分配员工"}')
                    return render(request, 'customers/customer_form.html', {'customer_form': customer_form, 'contact_form': contact_form})
                else:
                    customer = customer_form.save(commit=False)
                    if request.user.is_authenticated:
                        try:
                            employee = request.user.employee
                            customer.employee = employee
                            customer.save()
                            contact = contact_form.save(commit=False)
                            contact.customer = customer
                            contact.save()
                            print(f"创建客户成功，客户信息：{customer.company_name}, 负责员工：{customer.employee.user.username if customer.employee else '未分配'}")
                            return redirect('customer-list')
                        except AttributeError:
                            customer_form.add_error(None, '当前用户没有关联的员工信息')
                            print('当前用户没有关联的员工信息')
                            return render(request, 'customers/customer_form.html', {'customer_form': customer_form, 'contact_form': contact_form})
                    else:
                        customer_form.add_error(None, '用户未登录，请先登录')
                        logger.error('用户未登录')
                        return render(request, 'customers/customer_form.html', {'customer_form': customer_form, 'contact_form': contact_form})
            except Exception as e:
                logger.error(f'创建客户时出错：{e}')
                customer_form.add_error(None, f'创建客户时出错：{e}')
                return render(request, 'customers/customer_form.html', {'customer_form': customer_form, 'contact_form': contact_form})
        else:
            logger.error(f'表单验证失败：{customer_form.errors}')
            return render(request, 'customers/customer_form.html', {'customer_form': customer_form, 'contact_form': contact_form})


def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers/customer_list.html', {'customers': customers})


def customer_update(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
        contact = customer.contacts.first()
        if request.method == 'POST':
            customer_form = CustomerForm(request.POST, instance=customer)
            contact_form = ContactForm(request.POST, instance=contact)
            if customer_form.is_valid() and contact_form.is_valid():
                customer_form.save()
                contact_form.save()
                return redirect('customers:customer-list')
        else:
            customer_form = CustomerForm(instance=customer)
            contact_form = ContactForm(instance=contact)
        return render(request, 'customers/customer_form.html', {'customer_form': customer_form, 'contact_form': contact_form})
    except Customer.DoesNotExist:
        return redirect('customers:customer-list')


def customer_delete(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
        customer.delete()
        return redirect('customers:customer-list')
    except Customer.DoesNotExist:
        return redirect('customers:customer-list')


def customer_detail(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
        contacts = customer.contacts.all()
        return render(request, 'customers/customer_detail.html', {'customer': customer, 'contacts': contacts})
    except Customer.DoesNotExist:
        return redirect('customers:customer-list')
