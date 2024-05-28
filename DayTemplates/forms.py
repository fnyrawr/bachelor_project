from datetime import date

from django import forms

from .models import DayTemplate


class DayTemplateForm(forms.ModelForm):

    class Meta:
        model = DayTemplate
        fields = ['name', 'description']


class PasteTemplateForm(forms.ModelForm):
    to_date = forms.DateField()

    class Meta:
        model = DayTemplate
        fields = ['to_date']


class SearchForm(forms.ModelForm):
    keyword = forms.CharField(required=False)

    class Meta:
        model = DayTemplate
        fields = ['keyword']
