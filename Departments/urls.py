from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.department_list, name='departments'),
    path('create/', views.DepartmentCreationView.as_view(), name='create_department'),
    path('edit/<int:pk>', views.edit_department, name='edit_department'),
    path('delete/<int:pk>', views.delete_department, name='delete_department'),
]