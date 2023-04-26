from django.urls import path
from . import views

urlpatterns = [
    # Users
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('edit_basedata/', views.edit_basedata, name='edit_basedata'),
    path('useraccounts/', views.user_list, name='useraccounts'),
    path('create/', views.UserCreationView.as_view(), name='create_user'),
    path('edit/<int:pk>', views.edit_user, name='edit_user'),
    path('change_password/', views.change_password, name='change_password'),
    path('delete/<int:pk>', views.delete_user, name='delete_user'),
    path('employees/', views.employee_list, name='employees'),
    # EmployeesDepartments
    # path('show/<int:pk>/departments', ..., name='employee_departments'),
    # path('show/<int:pk1>/departments/<int:pk2>/create', ..., name='create_employee_department'),
    # path('show/<int:pk1>/departments/<int:pk2>/edit', ..., name='edit_employee_department'),
    # path('show/<int:pk1>/departments/<int:pk2>/delete', ..., name='delete_employee_department'),
]