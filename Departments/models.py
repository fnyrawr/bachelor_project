from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name + ' / ' + self.description
