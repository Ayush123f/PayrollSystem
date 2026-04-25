from django.urls import path
from . import views

urlpatterns = [
    path('',                        views.attendance_list,  name='attendance_list'),
    path('mark/',                   views.mark_attendance,  name='attendance_mark'),
    path('<int:pk>/edit/',          views.edit_attendance,  name='attendance_edit'),
    path('export/',                 views.export_attendance,name='attendance_export'),
    path('leave/',                  views.leave_list,       name='leave_list'),
    path('leave/apply/',            views.leave_apply,      name='leave_apply'),
    path('leave/<int:pk>/approve/', views.leave_approve,    name='leave_approve'),
    path('leave/<int:pk>/reject/',  views.leave_reject,     name='leave_reject'),
]