import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from rest_framework import serializers, viewsets, permissions
from rest_framework_api_key.permissions import HasAPIKey

from Departments.models import Department
from Qualifications.models import Qualification


class User(AbstractUser):
    ROLES = [
        ('A', 'Admin'),
        ('P', 'Planning Manager'),
        ('E', 'Employee'),
    ]
    username = models.CharField(max_length=15, blank=False, unique=True)
    staff_id = models.CharField(max_length=15, blank=False, unique=True)
    is_external = models.BooleanField(default=False)
    last_name = models.CharField(max_length=50, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(blank=False, unique=True)
    telephone_home = models.CharField(max_length=20, blank=True)
    telephone_mobile = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=50, blank=True)
    zip_city = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    role = models.CharField(max_length=1, choices=ROLES, default='E')
    is_verified = models.BooleanField(default=False)
    start_contract = models.DateField(default=timezone.now)
    end_contract = models.DateField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, blank=True, null=True)
    work_hours = models.IntegerField(blank=True, null=True)
    holiday_count = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['last_name', 'first_name', 'start_contract']

    def get_qualifications(self):
        return EmployeesQualifications.objects.filter(employee=self)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def __repr__(self):
        return self.first_name + ' / ' + self.last_name + ' / ' + self.email

    def is_authorized(self):
        # check for restricted access areas
        if self.role == 'A' or self.role == 'P':
            return True
        else:
            return False

    def is_admin(self):
        if self.role == 'A':
            return True
        else:
            return False


class EmployeesQualifications(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE)
    date_from = models.DateField(default=timezone.now)
    date_to = models.DateField(default=None, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='user_created_by', on_delete=models.DO_NOTHING, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    changed_by = models.ForeignKey(User, related_name='user_changed_by', on_delete=models.DO_NOTHING, blank=True)
    changed_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['employee', 'qualification', 'date_from']
        verbose_name = 'EmployeeQualification'
        verbose_name_plural = 'EmployeeQualifications'

    def is_active(self, date=datetime.datetime.today().date()):
        if date < self.date_from:
            return False
        if self.date_to:
            if self.date_to < date:
                return False
        return True

    def __str__(self):
        return self.employee.first_name + ' ' + self.employee.last_name + ' in ' + self.qualification.name

    def __repr__(self):
        return self.employee.username + ' / ' + self.qualification.name


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'staff_id', 'last_name', 'first_name', 'email', 'is_superuser', 'role', 'is_staff',
                  'is_active', 'date_joined', 'last_login']


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('staff_id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser | HasAPIKey]
