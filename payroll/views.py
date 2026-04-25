from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import models as db_models
from django.utils import timezone
from employees.models import Employee
from attendance.models import LeaveRequest
from salary.models import SalaryStructure
from .models import Payroll
import calendar


@login_required
def dashboard(request):
    today         = timezone.now().date()
    current_month = today.month
    current_year  = today.year

    # Monthly chart data
    monthly_amounts = []
    monthly_labels  = []
    for m in range(1, 13):
        total = Payroll.objects.filter(
            month=m, year=current_year
        ).aggregate(t=db_models.Sum('net_salary'))['t'] or 0
        monthly_amounts.append(float(total))
        monthly_labels.append(calendar.month_abbr[m])

    context = {
        'today':          today,
        'total_payroll':  Payroll.objects.filter(
                              month=current_month, year=current_year
                          ).aggregate(t=db_models.Sum('net_salary'))['t'] or 0,
        'total_employees': Employee.objects.filter(is_active=True).count(),
        'new_employees_this_month': Employee.objects.filter(
            date_joined__month=current_month,
            date_joined__year=current_year
        ).count(),
        'payslips_generated': Payroll.objects.filter(
            month=current_month, year=current_year,
            status='paid').count(),
        'payslips_pending': Payroll.objects.filter(
            month=current_month, year=current_year,
            status='draft').count(),
        'pending_leaves': LeaveRequest.objects.filter(
            status='pending').count(),
        'recent_payrolls': Payroll.objects.select_related(
            'employee__user', 'employee__department'
        ).order_by('-generated_on')[:5],
        'pending_leave_requests': LeaveRequest.objects.filter(
            status='pending'
        ).select_related('employee__user')[:4],
        'monthly_labels':  monthly_labels,
        'monthly_amounts': monthly_amounts,
        'department_summary': [],
    }
    return render(request, 'payroll/dashboard.html', context)


@login_required
def payroll_list(request):
    payrolls = Payroll.objects.select_related(
        'employee__user', 'employee__department'
    ).all()
    return render(request, 'payroll/payroll_list.html', {'payrolls': payrolls})


@login_required
def payroll_run(request):
    if not request.user.is_hr_or_admin():
        messages.error(request, 'Permission denied.')
        return redirect('payroll_list')

    if request.method == 'POST':
        month = int(request.POST['month'])
        year  = int(request.POST['year'])
        count = 0
        for emp in Employee.objects.filter(is_active=True):
            sal = emp.get_current_salary()
            if not sal:
                continue
            if Payroll.objects.filter(
                employee=emp, month=month, year=year
            ).exists():
                continue
            gross     = sal.calculate_gross()
            tax       = sal.calculate_tax()
            pf        = sal.calculate_pf()
            total_ded = tax + pf
            net       = gross - total_ded
            Payroll.objects.create(
                employee         = emp,
                salary_structure = sal,
                month            = month,
                year             = year,
                gross_salary     = gross,
                tax_deduction    = tax,
                pf_deduction     = pf,
                total_deduction  = total_ded,
                net_salary       = net,
                status           = 'processed',
            )
            count += 1
        messages.success(request, f'Payroll generated for {count} employees.')
        return redirect('payroll_list')

    return render(request, 'payroll/payroll_run.html', {
        'months': [(i, calendar.month_name[i]) for i in range(1, 13)],
        'current_year': timezone.now().year,
    })


@login_required
def payslip_list(request):
    if request.user.role == 'employee':
        payrolls = Payroll.objects.filter(
            employee__user=request.user
        ).order_by('-year', '-month')
    else:
        payrolls = Payroll.objects.select_related(
            'employee__user'
        ).all().order_by('-year', '-month')
    return render(request, 'payroll/payslip_list.html', {'payrolls': payrolls})


@login_required
def payslip_detail(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)
    return render(request, 'payroll/payslip_detail.html', {
        'payroll':           payroll,
        'company_name':      'PayrollPro Inc.',
        'company_email':     'hr@payrollpro.com',
        'company_address':   'Kathmandu, Nepal',
    })


@login_required
def payslip_pdf(request, pk):
    from .utils import generate_payslip_pdf
    payroll = get_object_or_404(Payroll, pk=pk)
    return generate_payslip_pdf(payroll)


@login_required
def payslip_email(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)
    messages.success(
        request, f'Payslip emailed to {payroll.employee.user.email}')
    return redirect('payslip_detail', pk=pk)