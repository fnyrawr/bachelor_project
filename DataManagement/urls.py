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
]
