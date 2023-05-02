from django.urls import path
from . import views

urlpatterns = [
    # Availabilities
    path('list/', views.availability_list, name='availabilities'),
    path('create/', views.AvailabilityCreationView.as_view(), name='create_availability'),
    path('edit/<int:pk>', views.edit_availability, name='edit_availability'),
    path('delete/<int:pk>', views.delete_availability, name='delete_availability'),
    path('list-own', views.own_availabilities, name='own_availabilities'),
]