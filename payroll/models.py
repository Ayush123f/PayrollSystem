from django.db import models
from employees.models import Employee
from salary.models import SalaryStructure
import calendar

MONTH_CHOICES = [(i, calendar.month_name[i]) for i in range(1, 13)]


class Payroll(models.Model):
    STATUS_CHOICES = [
        ('draft',     'Draft'),
        ('processed', 'Processed'),
        ('paid',      'Paid'),
    ]

    employee            = models.ForeignKey(Employee, on_delete=models.CASCADE,
                                            related_name='payrolls')
    salary_structure    = models.ForeignKey(SalaryStructure,
                                            on_delete=models.SET_NULL, null=True)
    month               = models.IntegerField(choices=MONTH_CHOICES)
    year                = models.IntegerField()
    gross_salary        = models.DecimalField(max_digits=10, decimal_places=2)
    tax_deduction       = models.DecimalField(max_digits=10, decimal_places=2,
                                              default=0)
    pf_deduction        = models.DecimalField(max_digits=10, decimal_places=2,
                                              default=0)
    insurance_deduction = models.DecimalField(max_digits=10, decimal_places=2,
                                              default=0)
    loan_deduction      = models.DecimalField(max_digits=10, decimal_places=2,
                                              default=0)
    leave_deduction     = models.DecimalField(max_digits=10, decimal_places=2,
                                              default=0)
    bonus               = models.DecimalField(max_digits=10, decimal_places=2,
                                              default=0)
    overtime_pay        = models.DecimalField(max_digits=10, decimal_places=2,
                                              default=0)
    total_deduction     = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary          = models.DecimalField(max_digits=10, decimal_places=2)
    working_days        = models.IntegerField(default=0)
    total_working_days  = models.IntegerField(default=26)
    leaves_taken        = models.IntegerField(default=0)
    status              = models.CharField(max_length=20, choices=STATUS_CHOICES,
                                           default='draft')
    generated_on        = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'month', 'year')
        ordering        = ['-year', '-month']

    def __str__(self):
        return f"{self.employee} | {self.get_month_display()} {self.year}"