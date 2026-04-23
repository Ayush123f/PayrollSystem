from django.contrib import admin
from .models import SalaryStructure


@admin.register(SalaryStructure)
class SalaryStructureAdmin(admin.ModelAdmin):
    list_display = ('employee', 'basic_salary', 'effective_from', 'is_active')
    list_filter  = ('is_active',)