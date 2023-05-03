from django.urls import path
from . import views

urlpatterns = [
    # Absences
    path('list/', views.absence_list, name='absences'),
    path('create/', views.AbsenceCreationView.as_view(), name='create_absence'),
    path('edit/<int:pk>', views.edit_absence, name='edit_absence'),
    path('delete/<int:pk>', views.delete_absence, name='delete_absence'),
    path('list-own', views.own_absences, name='own_absences'),
    path('add-own', views.OwnAbsenceCreationView.as_view(), name='add_own_absence'),
    path('edit-own/<int:pk>', views.edit_own_absence, name='edit_own_absence'),
    path('delete-own/<int:pk>', views.delete_own_absence, name='delete_own_absence'),
]
