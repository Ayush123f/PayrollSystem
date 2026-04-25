from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Attendance, LeaveRequest
from employees.models import Employee
import calendar as cal


@login_required
def attendance_list(request):
    today = timezone.now().date()
    month = int(request.GET.get('month', today.month))
    year  = int(request.GET.get('year',  today.year))

    _, num_days       = cal.monthrange(year, month)
    weekday_of_first  = cal.weekday(year, month, 1)

    status_map = {}
    if hasattr(request.user, 'employee'):
        for a in Attendance.objects.filter(
            employee=request.user.employee,
            date__month=month, date__year=year
        ):
            status_map[a.date.day] = a.status

    calendar_days = [{'blank': True}] * weekday_of_first
    for d in range(1, num_days + 1):
        from datetime import date
        date_obj = date(year, month, d)
        is_today = (date_obj == today)
        is_future = (date_obj > today)
        status = status_map.get(d, 'future' if is_future else 'holiday')
        calendar_days.append({
            'blank':  False,
            'day':    d,
            'status': 'today' if is_today else status,
        })

    if request.user.role == 'employee' and hasattr(request.user, 'employee'):
        today_records = Attendance.objects.filter(
            date=today
        ).select_related('employee__user', 'employee__department')
    else:
        today_records = Attendance.objects.filter(
            date=today
        ).select_related('employee__user', 'employee__department')

    att_qs = Attendance.objects.filter(date__month=month, date__year=year)
    if hasattr(request.user, 'employee'):
        att_qs = att_qs.filter(employee=request.user.employee)

    context = {
        'today':             today,
        'current_month':     month,
        'current_year':      year,
        'current_month_name': cal.month_name[month],
        'prev_month': 12 if month == 1 else month - 1,
        'prev_year':  year - 1 if month == 1 else year,
        'next_month': 1  if month == 12 else month + 1,
        'next_year':  year + 1 if month == 12 else year,
        'calendar_days':    calendar_days,
        'weekday_headers':  ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],
        'present_days':     att_qs.filter(status='present').count(),
        'absent_days':      att_qs.filter(status='absent').count(),
        'half_days':        att_qs.filter(status='half').count(),
        'holidays':         att_qs.filter(status='holiday').count(),
        'total_working_days': num_days,
        'attendance_percent': round(
            att_qs.filter(status='present').count() / max(num_days, 1) * 100, 1),
        'today_attendance': today_records,
        'today_present':    today_records.filter(status='present').count(),
        'today_total':      Employee.objects.filter(is_active=True).count(),
    }
    return render(request, 'attendance/attendance_list.html', context)


@login_required
def mark_attendance(request):
    if request.method == 'POST':
        Attendance.objects.update_or_create(
            employee_id = request.POST['employee'],
            date        = request.POST['date'],
            defaults={
                'status':    request.POST['status'],
                'check_in':  request.POST.get('check_in') or None,
                'check_out': request.POST.get('check_out') or None,
            }
        )
        messages.success(request, 'Attendance marked successfully.')
        return redirect('attendance_list')
    return render(request, 'attendance/mark_attendance.html', {
        'employees': Employee.objects.filter(is_active=True)
    })


@login_required
def edit_attendance(request, pk):
    record = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        record.status    = request.POST['status']
        record.check_in  = request.POST.get('check_in') or None
        record.check_out = request.POST.get('check_out') or None
        record.save()
        messages.success(request, 'Attendance updated.')
    return redirect('attendance_list')


@login_required
def leave_list(request):
    if request.user.role == 'employee':
        leaves = LeaveRequest.objects.filter(
            employee__user=request.user)
    else:
        leaves = LeaveRequest.objects.select_related(
            'employee__user').all()
    return render(request, 'attendance/leave_list.html', {'leaves': leaves})


@login_required
def leave_apply(request):
    if request.method == 'POST':
        emp = request.user.employee
        LeaveRequest.objects.create(
            employee   = emp,
            leave_type = request.POST['leave_type'],
            start_date = request.POST['start_date'],
            end_date   = request.POST['end_date'],
            reason     = request.POST.get('reason', ''),
        )
        messages.success(request, 'Leave request submitted.')
        return redirect('leave_list')
    return render(request, 'attendance/leave_apply.html')


@login_required
def leave_approve(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    leave.status = 'approved'
    leave.save()
    messages.success(request, f'Leave approved for {leave.employee}.')
    return redirect('dashboard')


@login_required
def leave_reject(request, pk):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    leave.status = 'rejected'
    leave.save()
    messages.warning(request, f'Leave rejected for {leave.employee}.')
    return redirect('dashboard')


@login_required
def export_attendance(request):
    import csv
    from django.http import HttpResponse
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance.csv"'
    writer = csv.writer(response)
    writer.writerow(['Employee', 'Date', 'Status', 'Check In', 'Check Out'])
    for a in Attendance.objects.select_related('employee__user').all():
        writer.writerow([
            a.employee.user.get_full_name(),
            a.date, a.status, a.check_in, a.check_out
        ])
    return response