from django.urls import path
from . import views

urlpatterns = [
    # Holidays
    path('list/', views.holiday_list, name='holidays'),
    path('create/', views.HolidayCreationView.as_view(), name='create_holiday'),
    path('edit/<int:pk>', views.edit_holiday, name='edit_holiday'),
    path('delete/<int:pk>', views.delete_holiday, name='delete_holiday'),
    path('list-own', views.own_holidays, name='own_holidays'),
    path('add-own', views.OwnHolidayCreationView.as_view(), name='add_own_holiday'),
    path('edit-own/<int:pk>', views.edit_own_holiday, name='edit_own_holiday'),
]