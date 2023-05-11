from django import forms

from Departments.models import Department
from Users.models import User
from .models import Shift


class ShiftForm(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all(),
                                        empty_label='Select department')
    employee = forms.ModelChoiceField(queryset=User.objects.all(),
                                      empty_label='Select employee', required=False)
    start = forms.DateTimeField(required=False)
    time = forms.DateTimeField(required=False)
    break_duration = forms.TimeField(initial='00:30')
    note = forms.Textarea(attrs={'required': False})

    class Meta:
        model = Shift
        fields = ['start', 'end', 'department', 'employee', 'break_duration', 'note']


class SearchForm(forms.ModelForm):
    filter_date = forms.DateField(required=False)
    keyword = forms.CharField(required=False)

    class Meta:
        model = Shift
        fields = ['filter_date', 'keyword']


class WorkHoursSearchForm(forms.ModelForm):
    filter_date = forms.DateField(required=False)
    employee = forms.ModelChoiceField(queryset=User.objects.all(),
                                      empty_label='Select employee')
    count_weeks = forms.IntegerField(initial=10)

    class Meta:
        model = Shift
        fields = ['filter_date', 'employee', 'count_weeks']


class ShiftplanSearchForm(forms.ModelForm):
    filter_date = forms.DateField(required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all(),
                                        empty_label='Select department')

    class Meta:
        model = Shift
        fields = ['filter_date', 'department']
