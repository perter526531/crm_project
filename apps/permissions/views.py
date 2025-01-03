from django.shortcuts import render
from django.views import View
from permissions.models import Permission

class PermissionListView(View):
    def get(self, request):
        permissions = Permission.objects.all()
        return render(request,'permissions/permission_list.html',{'permissions':permissions})