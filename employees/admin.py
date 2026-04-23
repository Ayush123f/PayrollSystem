from django.contrib import admin
from .models import Department, Designation, Employee


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display  = ('name', 'employee_count', 'created_at')
    search_fields = ('name',)


@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display  = ('title', 'department')
    list_filter   = ('department',)
    search_fields = ('title',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display  = ('employee_id', 'user', 'department',
                     'employee_type', 'is_active')
    list_filter   = ('department', 'employee_type', 'is_active')
    search_fields = ('employee_id', 'user__first_name', 'user__last_name')