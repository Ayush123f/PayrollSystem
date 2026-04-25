from django.urls import path
from . import views

urlpatterns = [
    path('',                         views.dashboard,      name='home'),
    path('dashboard/',               views.dashboard,      name='dashboard'),
    path('payroll/',                 views.payroll_list,   name='payroll_list'),
    path('payroll/run/',             views.payroll_run,    name='payroll_run'),
    path('payslips/',                views.payslip_list,   name='payslip_list'),
    path('payslips/<int:pk>/',       views.payslip_detail, name='payslip_detail'),
    path('payslips/<int:pk>/pdf/',   views.payslip_pdf,    name='payslip_pdf'),
    path('payslips/<int:pk>/email/', views.payslip_email,  name='payslip_email'),
]