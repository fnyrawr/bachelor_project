from django import forms

from .models import Department


class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ['name', 'description']

class SearchForm(forms.ModelForm):
    keyword = forms.CharField(required=False)

    class Meta:
        model = Department
        fields = ['keyword']
