from django import forms

from Users.models import User
from .models import Absence

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


class AbsenceForm(forms.ModelForm):
    employee = forms.ModelChoiceField(queryset=User.objects.all(),
                                      empty_label='Select employee')
    start_date = forms.DateField()
    end_date = forms.DateField()
    reason = forms.ChoiceField(choices=REASONS)
    status = forms.ChoiceField(choices=STATUS)
    note = forms.Textarea(attrs={'required': False})

    class Meta:
        model = Absence
        fields = ['employee', 'start_date', 'end_date', 'reason', 'status', 'note']
