from django.contrib import admin
from .models import Employee


# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'eid', 'phone', 'email', 'address', 'city', 'state', 'company', 'department')


admin.site.register(Employee, EmployeeAdmin)
