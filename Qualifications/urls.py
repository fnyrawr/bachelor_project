from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.qualification_list, name='qualifications'),
    path('create/', views.QualificationCreationView.as_view(), name='create_qualification'),
    path('show/<int:pk>/departments', views.view_qualification_departments, name='view_qualification_departments'),
    path('show/<int:pk>/employees', views.view_qualification_employees, name='view_qualification_employees'),
    path('edit/<int:pk>', views.edit_qualification, name='edit_qualification'),
    path('delete/<int:pk>', views.delete_qualification, name='delete_qualification'),
]