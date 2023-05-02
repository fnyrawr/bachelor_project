from django.db import models

from Users.models import User


class Absence(models.Model):
    REASONS = [
        (0, 'sickness (without medical proof'),
        (1, 'sickness (with medical proof)'),
        (2, 'private related'),
        (3, 'business related'),
        (4, 'other reason')
    ]
    STATUS = [
        (0, 'sent'),
        (1, 'not decided'),
        (2, 'declined'),
        (3, 'approved'),
    ]
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    start_day = models.DateField()
    end_day = models.DateField()
    reason = models.IntegerField(choices=REASONS, default=4)
    status = models.IntegerField(choices=STATUS, default=0)
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['employee', 'start_day', 'end_day']
        verbose_name = 'Absence'
        verbose_name_plural = 'Absences'

    def __str__(self):
        return self.employee + ' from ' + self.start_day + ' until ' + self.end_day + ' because of ' + self.reason

    def __repr__(self):
        return self.employee + ' / ' + self.start_day + ' / ' + self.end_day + ' / ' + self.reason +\
               ' / ' + self.status + ' / ' + self.note
