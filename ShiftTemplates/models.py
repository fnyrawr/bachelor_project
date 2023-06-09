from datetime import timedelta, datetime

from django.db import models

from Departments.models import Department
from Qualifications.models import Qualification


class ShiftTemplate(models.Model):
    name = models.CharField(max_length=30, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    break_duration = models.TimeField()
    note = models.TextField(blank=True)

    class Meta:
        ordering = ['department', 'name', 'start_time', 'end_time', 'break_duration']
        verbose_name = 'ShiftTemplate'
        verbose_name_plural = 'ShiftTemplates'

    def get_work_hours(self):
        # calculate actual work hours (end-start-break)
        start_time = timedelta(hours=self.start_time.hour, minutes=self.start_time.minute)
        end_time = timedelta(hours=self.end_time.hour, minutes=self.end_time.minute)
        if end_time < start_time:
            end_time += timedelta(days=1)
        work_hours = end_time - start_time
        if self.break_duration is not None:
            work_hours -= timedelta(hours=self.break_duration.hour, minutes=self.break_duration.minute)
        return (datetime.min + work_hours).time()

    def get_qualifications(self):
        qualifications = ShiftTemplateQualifications.objects.filter(shift_template=self)
        return qualifications

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name + ' / ' + self.note + ' / ' + self.department.name + ' / '\
               + str(self.start_time) + ' / ' + str(self.end_time)


class ShiftTemplateQualifications(models.Model):
    shift_template = models.ForeignKey(ShiftTemplate, on_delete=models.CASCADE)
    qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE)

    class Meta:
        ordering = ['shift_template', 'qualification']
        verbose_name = 'ShiftTemplateQualification'
        verbose_name_plural = 'ShiftTemplateQualifications'
