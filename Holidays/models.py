from django.db import models

from Users.models import User


class Holiday(models.Model):
    STATUS = [
        (0, 'sent'),
        (1, 'not decided'),
        (2, 'declined'),
        (3, 'approved'),
    ]
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    start_day = models.DateField()
    end_day = models.DateField()
    status = models.IntegerField(choices=STATUS, default=0)
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['employee', 'start_day', 'end_day']
        verbose_name = 'Holidays'
        verbose_name_plural = 'Holidays'

    def __str__(self):
        return self.employee + ' from ' + self.start_day + ' until ' + self.end_day

    def __repr__(self):
        return self.employee + ' / ' + self.start_day + ' / ' + self.end_day + ' / ' + self.status + ' / ' + self.note
