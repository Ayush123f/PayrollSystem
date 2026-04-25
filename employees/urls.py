from django.urls import path
from . import views

urlpatterns = [
    path('',                 views.EmployeeListView.as_view(), name='employee_list'),
    path('add/',             views.employee_add,               name='employee_add'),
    path('<int:pk>/',        views.employee_detail,            name='employee_detail'),
    path('<int:pk>/edit/',   views.employee_edit,              name='employee_edit'),
    path('<int:pk>/delete/', views.employee_delete,            name='employee_delete'),
    path('departments/',     views.department_list,            name='department_list'),
]