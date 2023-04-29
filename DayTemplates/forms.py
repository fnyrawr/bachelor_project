from django import forms

from .models import DayTemplate


class DayTemplateForm(forms.ModelForm):

    class Meta:
        model = DayTemplate
        fields = ['name', 'description']
