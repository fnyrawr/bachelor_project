from django.urls import path
from . import views

urlpatterns = [
    # Departments
    path('list/', views.department_list, name='departments'),
    path('create/', views.DepartmentCreationView.as_view(), name='create_department'),
    path('show/<int:pk>', views.view_department, name='view_department'),
    path('edit/<int:pk>', views.edit_department, name='edit_department'),
    path('delete/<int:pk>', views.delete_department, name='delete_department'),
    # DepartmentsQualifications
    path('show/<int:pk1>/add_qualification/<int:pk2>', views.add_qualification, name='add_department_qualification'),
    path('show/<int:pk1>/remove_qualification/<int:pk2>', views.remove_qualification,
         name='remove_department_qualification'),
]
