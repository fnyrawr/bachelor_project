from datetime import timedelta, datetime
from django.utils import timezone

from django.db import models

from Departments.models import Department
from Qualifications.models import Qualification
from Users.models import User


class Shift(models.Model):
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    employee = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField()
    break_duration = models.TimeField()
    note = models.TextField(blank=True)
    highlight = models.BooleanField(default=False)

    class Meta:
        ordering = ['start', 'end', 'department', 'break_duration', 'employee']
        verbose_name = 'Shift'
        verbose_name_plural = 'Shifts'

    def get_date(self):
        return self.start.date()

    def get_start_time(self):
        return self.start.time()

    def get_end_time(self):
        return self.end.time()

    def get_work_hours(self):
        # calculate actual work hours (end-start-break)
        if self.start < self.end:
            work_hours = self.end - self.start
        else:
            work_hours = datetime.max - self.start + self.end
        if self.break_duration is not None:
            work_hours -= timedelta(hours=self.break_duration.hour, minutes=self.break_duration.minute)
        return (datetime.min + work_hours).time()

    def get_qualifications(self):
        qualifications = ShiftQualifications.objects.filter(shift=self)
        return qualifications

    def __str__(self):
        return str(self.start.date()) + ' from ' + str(self.start.time()) + ' to ' + str(self.end.time())

    def __repr__(self):
        if self.employee:
            return str(self.start) + ' / ' + str(self.end) + ' / ' + self.department.name + ' / '\
               + self.employee.username + ' / ' + self.note
        else:
            return str(self.start) + ' / ' + str(self.end) + ' / ' + self.department.name + ' / ' + self.note


class ShiftQualifications(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE)

    class Meta:
        ordering = ['shift', 'qualification']
        verbose_name = 'ShiftQualification'
        verbose_name_plural = 'ShiftQualifications'
