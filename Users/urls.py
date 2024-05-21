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
    # EmployeesQualifications
    path('show/<int:pk1>/add_qualification/<int:pk2>', views.add_qualification, name='add_employee_qualification'),
    path('show/<int:pk1>/remove_qualification/<int:pk2>', views.remove_qualification, name='remove_employee_qualification'),
    # Attendance
    path('attendance/', views.attendance, name='attendance'),
    # HTMX
    path('create/check_username/', views.check_username, name='check_username'),
    # REST Endpoints
    path('', views.get_users, name='get_users'),
    path('<str:username>', views.get_user_by_username, name='get_user_by_username'),
]
