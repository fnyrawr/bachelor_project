from django import forms

from Users.models import User
from .models import Availability

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

WEEKDAYS_search = [
        (0, 'All'),
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    ]

TENDENCIES_search = [
        (-1, 'All'),
        (0, 'No preference'),
        (1, 'Early shift'),
        (2, 'Midday shift'),
        (3, 'Late shift'),
        (4, 'Night shift')
    ]


class AvailabilityForm(forms.ModelForm):
    employee = forms.ModelChoiceField(queryset=User.objects.all(),
                                      empty_label='Select employee')
    weekday = forms.ChoiceField(choices=WEEKDAYS)
    start_time = forms.TimeField(initial='12:00', required=False)
    end_time = forms.TimeField(initial='12:00', required=False)
    tendency = forms.ChoiceField(choices=TENDENCIES)
    is_available = forms.BooleanField(initial=True, required=False)
    note = forms.Textarea(attrs={'required': False})

    class Meta:
        model = Availability
        fields = ['employee', 'weekday', 'start_time', 'end_time', 'tendency', 'is_available', 'note']


class SearchForm(forms.ModelForm):
    filter_weekday = forms.ChoiceField(choices=WEEKDAYS_search)
    filter_tendency = forms.ChoiceField(choices=TENDENCIES_search)
    filter_is_available = forms.BooleanField(initial=True, required=False)
    keyword = forms.CharField(required=False)

    class Meta:
        model = Availability
        fields = ['filter_weekday', 'filter_is_available', 'filter_tendency', 'keyword']
