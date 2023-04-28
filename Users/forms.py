from datetime import date

from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django import forms

from Departments.models import Department
from .models import User


class CustomUserForm(UserCreationForm):
    staff_id = forms.CharField(max_length=15)
    telephone_home = forms.CharField(max_length=20, required=False)
    telephone_mobile = forms.CharField(max_length=20, required=False)
    address = forms.CharField(max_length=50, required=False)
    zip_city = forms.CharField(max_length=50, required=False)
    role = forms.CharField(max_length=1)
    start_contract = forms.DateField(required=False, initial=date.today())
    end_contract = forms.DateField(required=False)
    work_hours = forms.IntegerField(required=False)
    holiday_count = forms.IntegerField(required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), to_field_name='name',
                                        empty_label='Select department', required=False)

    class Meta:
        model = User
        fields = ['username',
                  'staff_id',
                  'is_external',
                  'last_name',
                  'first_name',
                  'email',
                  'telephone_home',
                  'telephone_mobile',
                  'address',
                  'zip_city',
                  'role',
                  'is_active',
                  'is_verified',
                  'start_contract',
                  'end_contract',
                  'work_hours',
                  'holiday_count',
                  'department'
                  ]


class SetPasswordFormImpl(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
