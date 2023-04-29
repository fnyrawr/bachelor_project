from django.db import models

from Departments.models import Department


class Demand(models.Model):
    WEEKDAYS = [
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    ]
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    weekday = models.IntegerField(choices=WEEKDAYS, default=1)
    start_time = models.TimeField()
    end_time = models.TimeField()
    staff_count = models.IntegerField()
    note = models.TextField(blank=True)

    class Meta:
        ordering = ['department', 'weekday', 'start_time', 'end_time']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.department + ' on ' + self.get_weekday_display() + ' between ' +\
               self.start_time + ' and ' + self.end_time

    def __repr__(self):
        return self.department + ' / ' + self.weekday + ' / ' + self.start_time + ' / ' + self.end_time +\
               ' / ' + self.staff_count
