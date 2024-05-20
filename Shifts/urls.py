from django.urls import path
from . import views

urlpatterns = [
    # Shifts
    path('list/', views.shift_list, name='shifts'),
    path('shiftplan/', views.shiftplan, name='shiftplan'),
    path('work_hours/', views.work_hours, name='work_hours'),
    path('own/', views.own_shifts, name='own_shifts'),
    path('create/', views.ShiftCreationView.as_view(), name='create_shift'),
    path('edit/<int:pk>', views.edit_shift, name='edit_shift'),
    path('assign/<int:pk1>/employee/<int:pk2>', views.assign_employee, name='assign_employee'),
    path('remove/<int:pk>', views.remove_employee, name='remove_employee'),
    path('delete/<int:pk>', views.delete_shift, name='delete_shift'),
    # ShiftQualifications
    path('show/<int:pk1>/add_qualification/<int:pk2>', views.add_qualification,
         name='add_shift_qualification'),
    path('show/<int:pk1>/remove_qualification/<int:pk2>', views.remove_qualification,
         name='remove_shift_qualification'),
    # HTMX
    path('search_own_shifts/', views.search_own_shifts, name='search_own_shifts'),
]