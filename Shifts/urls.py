from django.urls import path
from . import views

urlpatterns = [
    # Shifts
    path('list/', views.shift_list, name='shifts'),
    path('create/', views.ShiftCreationView.as_view(), name='create_shift'),
    # path('show/<int:pk>', views.view_shift, name='view_shift'),
    path('edit/<int:pk>', views.edit_shift, name='edit_shift'),
    path('delete/<int:pk>', views.delete_shift, name='delete_shift'),
    # ShiftQualifications
    path('show/<int:pk1>/add_qualification/<int:pk2>', views.add_qualification,
         name='add_shift_qualification'),
    path('show/<int:pk1>/remove_qualification/<int:pk2>', views.remove_qualification,
         name='remove_shift_qualification'),
]