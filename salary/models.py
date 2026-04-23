from django.db import models
from employees.models import Employee


class SalaryStructure(models.Model):
    employee       = models.ForeignKey(
                         Employee, on_delete=models.CASCADE,
                         related_name='salary_structures')
    basic_salary   = models.DecimalField(max_digits=10, decimal_places=2)
    hra            = models.DecimalField(max_digits=10, decimal_places=2,
                                         default=0)
    allowances     = models.DecimalField(max_digits=10, decimal_places=2,
                                         default=0)
    pf_percentage  = models.DecimalField(max_digits=5, decimal_places=2,
                                         default=12.0)
    tax_rate       = models.DecimalField(max_digits=5, decimal_places=2,
                                         default=10.0)
    effective_from = models.DateField()
    is_active      = models.BooleanField(default=True)

    def __str__(self):
        return f"Salary - {self.employee} (from {self.effective_from})"

    # ── OOP Calculation Methods ───────────────

    def calculate_gross(self):
        return self.basic_salary + self.hra + self.allowances

    def calculate_pf(self):
        return round((self.basic_salary * self.pf_percentage) / 100, 2)

    def calculate_tax(self):
        return round((self.calculate_gross() * self.tax_rate) / 100, 2)

    def calculate_total_deductions(self):
        return self.calculate_pf() + self.calculate_tax()

    def calculate_net(self):
        return self.calculate_gross() - self.calculate_total_deductions()