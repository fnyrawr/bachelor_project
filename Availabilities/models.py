from django.db import models

from Users.models import User


class Availability(models.Model):
    WEEKDAYS = [
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    ]
    TENDENCIES = [
        (0, 'No preference'),
        (1, 'Early shift'),
        (2, 'Midday shift'),
        (3, 'Late shift'),
        (4, 'Night shift')
    ]
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    weekday = models.IntegerField(choices=WEEKDAYS, default=1)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    tendency = models.IntegerField(choices=TENDENCIES, default=0)
    is_available = models.BooleanField(default=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-is_available', 'weekday', 'tendency', 'start_time', 'end_time', 'employee']
        verbose_name = 'Availability'
        verbose_name_plural = 'Availabilities'

    def get_availability(self):
        return self.is_available

    def get_preference(self):
        return self.get_tendency_display()

    def get_start_time(self):
        if self.start_time:
            return str(self.start_time.strftime('%H:%M'))
        return None

    def get_end_time(self):
        if self.end_time:
            return str(self.end_time.strftime('%H:%M'))
        return None

    def __str__(self):
        return self.employee + ' on ' + self.get_weekday_display() + ' is available ' + self.is_available

    def __repr__(self):
        return self.employee + ' / ' + self.weekday + ' / ' + self.start_time + ' / ' + self.end_time +\
               ' / ' + self.is_available + ' / ' + self.get_tendency_display()
