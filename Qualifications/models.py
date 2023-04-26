from django.db import models


class Qualification(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(blank=True)
    is_important = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Qualification'
        verbose_name_plural = 'Qualifications'

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name + ' / ' + self.description + ' / Important: ' + str(self.is_important)
