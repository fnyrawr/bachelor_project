from django import forms

from .models import Qualification


class QualificationForm(forms.ModelForm):

    class Meta:
        model = Qualification
        fields = ['name', 'description', 'is_important']


class SearchForm(forms.ModelForm):
    keyword = forms.CharField(required=False)

    class Meta:
        model = Qualification
        fields = ['keyword']
