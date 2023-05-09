from django import forms

from Users.models import User
from .models import Absence

REASONS = [
    (0, 'sickness (without medical proof)'),
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

REASONS_search = [
    (-1, 'all'),
    (0, 'sickness (without medical proof)'),
    (1, 'sickness (with medical proof)'),
    (2, 'private related'),
    (3, 'business related'),
    (4, 'other reason')
]

STATUS_search = [
    (-1, 'all'),
    (0, 'sent'),
    (1, 'not decided'),
    (2, 'declined'),
    (3, 'approved'),
]

MONTHS = [
    (0, 'All'),
    (1, 'January'),
    (2, 'February'),
    (3, 'March'),
    (4, 'April'),
    (5, 'May'),
    (6, 'June'),
    (7, 'July'),
    (8, 'August'),
    (9, 'September'),
    (10, 'October'),
    (11, 'November'),
    (12, 'December'),
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


class SearchForm(forms.ModelForm):
    filter_year = forms.CharField(max_length=4, required=False)
    filter_month = forms.ChoiceField(choices=MONTHS)
    filter_date = forms.DateField(required=False)
    keyword = forms.CharField(required=False)
    filter_status = forms.ChoiceField(choices=STATUS_search)
    filter_reason = forms.ChoiceField(choices=REASONS_search)

    class Meta:
        model = User
        fields = ['filter_year', 'filter_month', 'filter_date', 'filter_status', 'filter_reason', 'keyword']
