from django.db import models
from accounts.models import CustomUser

AVATAR_COLORS = [
    '#e94560', '#3b82f6', '#22c55e',
    '#f59e0b', '#8b5cf6', '#06b6d4',
]


class Department(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def employee_count(self):
        return self.employee_set.filter(is_active=True).count()


class Designation(models.Model):
    title      = models.CharField(max_length=100)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='designations'
    )

    def __str__(self):
        return f"{self.title} ({self.department.name})"


class Employee(models.Model):
    EMPLOYEE_TYPES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract',  'Contract'),
    ]

    user          = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    employee_id   = models.CharField(max_length=20, unique=True)
    department    = models.ForeignKey(
                        Department, on_delete=models.SET_NULL,
                        null=True, blank=True)
    designation   = models.ForeignKey(
                        Designation, on_delete=models.SET_NULL,
                        null=True, blank=True)
    employee_type = models.CharField(max_length=20, choices=EMPLOYEE_TYPES,
                                     default='full_time')
    date_joined        = models.DateField()
    phone              = models.CharField(max_length=15, blank=True)
    address            = models.TextField(blank=True)
    photo              = models.ImageField(upload_to='employee_photos/',
                                           blank=True, null=True)
    bank_account_last4 = models.CharField(max_length=4, blank=True)
    is_active          = models.BooleanField(default=True)

    class Meta:
        ordering = ['employee_id']

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name()}"

    @property
    def initials(self):
        f = self.user.first_name[:1].upper()
        l = self.user.last_name[:1].upper()
        return f"{f}{l}"

    @property
    def avatar_color(self):
        index = sum(ord(c) for c in self.employee_id) % len(AVATAR_COLORS)
        return AVATAR_COLORS[index]

    def get_current_salary(self):
        return self.salary_structures.filter(is_active=True).first()