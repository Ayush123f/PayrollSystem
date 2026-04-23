from django.contrib import admin
from .models import Attendance, LeaveRequest


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display  = ('employee', 'date', 'status', 'check_in', 'check_out')
    list_filter   = ('status', 'date')
    search_fields = ('employee__user__first_name', 'employee__user__last_name')


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display  = ('employee', 'leave_type', 'start_date', 'end_date', 'status')
    list_filter   = ('status', 'leave_type')