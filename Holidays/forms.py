from django import forms

from Users.models import User
from .models import Holiday

STATUS = [
    (0, 'sent'),
    (1, 'not decided'),
    (2, 'declined'),
    (3, 'approved'),
]


class HolidayForm(forms.ModelForm):
    employee = forms.ModelChoiceField(queryset=User.objects.all(),
                                      empty_label='Select employee')
    start_date = forms.DateField()
    end_date = forms.DateField()
    status = forms.ChoiceField(choices=STATUS)
    note = forms.Textarea(attrs={'required': False})

    class Meta:
        model = Holiday
        fields = ['employee', 'start_date', 'end_date', 'status', 'note']
