from django.db import models
from datetime import datetime

from Users.models import User


class Wish(models.Model):
    TENDENCIES = [
        (0, 'No preference'),
        (1, 'Early shift'),
        (2, 'Midday shift'),
        (3, 'Late shift'),
        (4, 'Night shift')
    ]
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.today())
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    tendency = models.IntegerField(choices=TENDENCIES, default=0)
    is_available = models.BooleanField(default=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['date', '-is_available', 'tendency', 'start_time', 'end_time', 'employee']
        verbose_name = 'Wish'
        verbose_name_plural = 'Wishes'

    def __str__(self):
        return self.employee + ' on ' + self.date + ' is available ' + self.is_available

    def __repr__(self):
        return self.employee + ' / ' + self.date + ' / ' + self.start_time + ' / ' + self.end_time +\
               ' / ' + self.is_available + ' / ' + self.get_tendency_display()
