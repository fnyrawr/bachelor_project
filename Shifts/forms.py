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
