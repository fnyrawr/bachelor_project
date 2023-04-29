from django import forms

from Departments.models import Department
from .models import ShiftTemplate


class ShiftTemplateForm(forms.ModelForm):
    name = forms.CharField(max_length=30)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), to_field_name='name',
                                        empty_label='Select department')
    start_time = forms.TimeField(initial='12:00')
    end_time = forms.TimeField(initial='18:00')
    break_duration = forms.TimeField(initial='00:30')
    note = forms.Textarea(attrs={'required': False})

    class Meta:
        model = ShiftTemplate
        fields = ['name', 'department', 'start_time', 'end_time', 'break_duration', 'note']
