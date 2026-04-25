from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from employees.models import Employee, Department


@login_required
def reports_dashboard(request):
    departments = []
    for dept in Department.objects.all():
        emps = Employee.objects.filter(department=dept, is_active=True)
        total = sum(
            float(e.get_current_salary().calculate_gross())
            for e in emps if e.get_current_salary()
        )
        avg = total / emps.count() if emps.count() else 0
        departments.append({
            'name':         dept.name,
            'headcount':    emps.count(),
            'total_salary': total,
            'avg_salary':   avg,
        })
    return render(request, 'reports/reports.html', {
        'departments':     departments,
        'total_employees': Employee.objects.filter(is_active=True).count(),
    })