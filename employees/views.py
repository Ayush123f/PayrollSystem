from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Employee, Department, Designation
from accounts.models import CustomUser
from salary.models import SalaryStructure


class EmployeeListView(LoginRequiredMixin, ListView):
    model               = Employee
    template_name       = 'employees/employee_list.html'
    context_object_name = 'employees'
    paginate_by         = 10

    def get_queryset(self):
        qs    = Employee.objects.select_related(
                    'user', 'department', 'designation')
        q     = self.request.GET.get('q', '')
        dept  = self.request.GET.get('department', '')
        etype = self.request.GET.get('type', '')
        status= self.request.GET.get('status', '')
        if q:
            qs = qs.filter(
                Q(user__first_name__icontains=q) |
                Q(user__last_name__icontains=q)  |
                Q(employee_id__icontains=q)
            )
        if dept:   qs = qs.filter(department__pk=dept)
        if etype:  qs = qs.filter(employee_type=etype)
        if status == 'active':   qs = qs.filter(is_active=True)
        if status == 'inactive': qs = qs.filter(is_active=False)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['departments']  = Department.objects.all()
        ctx['total_count']  = Employee.objects.count()
        ctx['active_count'] = Employee.objects.filter(is_active=True).count()
        params = self.request.GET.copy()
        params.pop('page', None)
        ctx['query_params'] = params.urlencode()
        return ctx


@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/employee_detail.html',
                  {'employee': employee})


@login_required
def employee_add(request):
    if request.method == 'POST':
        user = CustomUser.objects.create_user(
            username   = request.POST['username'],
            password   = request.POST['password'],
            first_name = request.POST['first_name'],
            last_name  = request.POST['last_name'],
            email      = request.POST['email'],
            role       = request.POST.get('role', 'employee'),
        )
        emp = Employee.objects.create(
            user           = user,
            employee_id    = request.POST['employee_id'],
            department_id  = request.POST['department'],
            designation_id = request.POST.get('designation'),
            employee_type  = request.POST['employee_type'],
            date_joined    = request.POST['date_joined'],
            phone          = request.POST.get('phone', ''),
            address        = request.POST.get('address', ''),
        )
        if request.FILES.get('photo'):
            emp.photo = request.FILES['photo']
            emp.save()
        SalaryStructure.objects.create(
            employee       = emp,
            basic_salary   = request.POST['basic_salary'],
            hra            = request.POST.get('hra', 0),
            allowances     = request.POST.get('allowances', 0),
            pf_percentage  = request.POST.get('pf_percentage', 12),
            tax_rate       = request.POST.get('tax_rate', 10),
            effective_from = request.POST['date_joined'],
            is_active      = True,
        )
        messages.success(request, f'Employee {emp} added successfully.')
        return redirect('employee_list')

    return render(request, 'employees/employee_form.html', {
        'departments':  Department.objects.all(),
        'designations': Designation.objects.all(),
    })


@login_required
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        u = employee.user
        u.first_name = request.POST['first_name']
        u.last_name  = request.POST['last_name']
        u.email      = request.POST['email']
        u.save()
        employee.department_id  = request.POST['department']
        employee.designation_id = request.POST.get('designation')
        employee.employee_type  = request.POST['employee_type']
        employee.phone          = request.POST.get('phone', '')
        employee.address        = request.POST.get('address', '')
        employee.is_active      = request.POST.get('is_active') == 'true'
        if request.FILES.get('photo'):
            employee.photo = request.FILES['photo']
        employee.save()
        messages.success(request, 'Employee updated successfully.')
        return redirect('employee_detail', pk=pk)

    return render(request, 'employees/employee_form.html', {
        'employee':     employee,
        'departments':  Department.objects.all(),
        'designations': Designation.objects.all(),
    })


@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.user.delete()
        messages.success(request, 'Employee deleted.')
        return redirect('employee_list')
    return render(request, 'employees/employee_confirm_delete.html',
                  {'employee': employee})


@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'employees/department_list.html',
                  {'departments': departments})