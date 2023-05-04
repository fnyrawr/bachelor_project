from django.db import models
from datetime import timedelta
from django.utils import timezone

from Users.models import User


class Holiday(models.Model):
    STATUS = [
        (0, 'sent'),
        (1, 'not decided'),
        (2, 'declined'),
        (3, 'approved'),
    ]
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    status = models.IntegerField(choices=STATUS, default=0)
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['start_date', 'end_date', 'employee']
        verbose_name = 'Holidays'
        verbose_name_plural = 'Holidays'

    def get_duration(self):
        # calculate holiday duration in days
        start_date = self.start_date
        end_date = self.end_date
        duration = end_date - start_date + timedelta(days=1)
        return duration.days

    def __str__(self):
        return self.employee + ' from ' + self.start_date + ' until ' + self.end_date

    def __repr__(self):
        return self.employee + ' / ' + self.start_date + ' / ' + self.end_date + ' / ' + self.status + ' / ' + self.note
