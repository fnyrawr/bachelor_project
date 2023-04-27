from django.db import models

from Qualifications.models import Qualification


class Department(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def get_employees(self):
        # use User class only here to avoid circular import issues
        from Users.models import User
        employees = User.objects.filter(department=self)
        return employees

    def get_work_hours(self):
        # use User class only here to avoid circular import issues
        from Users.models import User
        employees = User.objects.filter(department=self)
        work_hours = 0
        for employee in employees:
            if employee.work_hours is not None:
                work_hours += employee.work_hours
        return work_hours

    def get_qualifications(self):
        qualifications = DepartmentQualifications.objects.filter(department=self)
        return qualifications

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name + ' / ' + self.description


class DepartmentQualifications(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE)

    class Meta:
        ordering = ['department', 'qualification']
        verbose_name = 'DepartmentQualification'
        verbose_name_plural = 'DepartmentQualifications'
