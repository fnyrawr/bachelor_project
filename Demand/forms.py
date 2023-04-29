from datetime import date

from django import forms

from Departments.models import Department
from .models import Demand

WEEKDAYS = [
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    ]


class DemandForm(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), to_field_name='name',
                                        empty_label='Select department')
    weekday = forms.ChoiceField(choices=WEEKDAYS)
    start_time = forms.TimeField(initial='12:00')
    end_time = forms.TimeField(initial='12:00')
    staff_count = forms.IntegerField(initial=1)
    note = forms.Textarea(attrs={'required': False})

    class Meta:
        model = Demand
        fields = ['department', 'weekday', 'start_time', 'end_time', 'staff_count', 'note']
