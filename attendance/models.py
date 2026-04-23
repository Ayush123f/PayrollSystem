from django.db import models
from employees.models import Employee
from datetime import datetime


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent',  'Absent'),
        ('half',    'Half Day'),
        ('holiday', 'Holiday'),
    ]
    employee  = models.ForeignKey(Employee, on_delete=models.CASCADE,
                                  related_name='attendances')
    date      = models.DateField()
    status    = models.CharField(max_length=10, choices=STATUS_CHOICES,
                                 default='present')
    check_in  = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)

    class Meta:
        unique_together = ('employee', 'date')
        ordering        = ['-date']

    def __str__(self):
        return f"{self.employee} - {self.date} - {self.status}"

    @property
    def hours_worked(self):
        if self.check_in and self.check_out:
            dt_in  = datetime.combine(self.date, self.check_in)
            dt_out = datetime.combine(self.date, self.check_out)
            return (dt_out - dt_in).seconds / 3600
        return 0

    @property
    def hours_formatted(self):
        h = self.hours_worked
        return f"{int(h)}h {int((h % 1) * 60)}m"


class LeaveRequest(models.Model):
    LEAVE_TYPES = [
        ('sick',   'Sick Leave'),
        ('casual', 'Casual Leave'),
        ('annual', 'Annual Leave'),
    ]
    STATUS_CHOICES = [
        ('pending',  'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    DOT_COLORS = {
        'sick':   '#f59e0b',
        'casual': '#3b82f6',
        'annual': '#8b5cf6',
    }

    employee   = models.ForeignKey(Employee, on_delete=models.CASCADE,
                                   related_name='leave_requests')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date   = models.DateField()
    reason     = models.TextField(blank=True)
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES,
                                  default='pending')
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee} - {self.get_leave_type_display()} ({self.status})"

    @property
    def days(self):
        return (self.end_date - self.start_date).days + 1

    @property
    def dot_color(self):
        return self.DOT_COLORS.get(self.leave_type, '#94a3b8')