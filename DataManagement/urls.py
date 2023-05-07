from django.urls import path
from . import views

urlpatterns = [
    # Data management
    path('', views.data_management, name='datamanagement'),
    path('qualifications/', views.import_qualifications, name='import_qualifications'),
    path('departments/', views.import_departments, name='import_departments'),
    path('users/', views.import_users, name='import_users'),
    path('absences/', views.import_absences, name='import_absences'),
    path('holidays/', views.import_holidays, name='import_holidays'),
    path('demand/', views.import_demand, name='import_demand'),
    path('availabilities/', views.import_availabilities, name='import_availabilities'),
    path('wishes/', views.import_wishes, name='import_wishes'),
    path('shift_templates/', views.import_shift_templates, name='import_shift_templates'),
    path('day_templates/', views.import_day_templates, name='import_day_templates'),
    path('shifts/', views.import_shifts, name='import_shifts'),
]
