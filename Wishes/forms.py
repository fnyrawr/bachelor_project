from django import forms

from Users.models import User
from .models import Wish

TENDENCIES = [
        (0, 'No preference'),
        (1, 'Early shift'),
        (2, 'Midday shift'),
        (3, 'Late shift'),
        (4, 'Night shift')
    ]


class WishForm(forms.ModelForm):
    employee = forms.ModelChoiceField(queryset=User.objects.all(),
                                      empty_label='Select employee')
    date = forms.DateField()
    start_time = forms.TimeField(required=False)
    end_time = forms.TimeField(required=False)
    tendency = forms.ChoiceField(choices=TENDENCIES)
    is_available = forms.BooleanField(initial=True, required=False)
    note = forms.Textarea(attrs={'required': False})

    class Meta:
        model = Wish
        fields = ['employee', 'date', 'start_time', 'end_time', 'tendency', 'is_available', 'note']
