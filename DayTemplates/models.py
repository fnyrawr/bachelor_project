from django.db import models

from ShiftTemplates.models import ShiftTemplate


class DayTemplate(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'DayTemplate'
        verbose_name_plural = 'DayTemplates'

    def get_shifts(self):
        shifts = DayShiftTemplates.objects.filter(day_template=self)
        return shifts

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name + ' / ' + self.description


class DayShiftTemplates(models.Model):
    day_template = models.ForeignKey(DayTemplate, on_delete=models.CASCADE)
    shift_template = models.ForeignKey(ShiftTemplate, on_delete=models.CASCADE)

    class Meta:
        ordering = ['day_template', 'shift_template']
        verbose_name = 'DayShiftTemplate'
        verbose_name_plural = 'DayShiftTemplates'
