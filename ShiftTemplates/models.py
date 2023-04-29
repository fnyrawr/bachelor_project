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
        work_hours = self.end_time-self.start_time
        if self.break_duration is not None:
            work_hours -= self.break_duration
        return work_hours

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
