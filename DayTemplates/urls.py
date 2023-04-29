from django.urls import path
from . import views

urlpatterns = [
    # DayTemplates
    # path('list/', views.day_template_list, name='day_templates'),
    # path('create/', views.DayTemplateCreationView.as_view(), name='create_day_template'),
    # path('show/<int:pk>', views.view_day_template, name='view_day_template'),
    # path('edit/<int:pk>', views.edit_day_template, name='edit_day_template'),
    # path('delete/<int:pk>', views.delete_day_template, name='delete_day_template'),
    # DayShiftTemplates
    # path('show/<int:pk1>/add_shift_template/<int:pk2>', views.add_shift_template,
    #      name='add_shift_template'),
    # path('show/<int:pk1>/remove_qualification/<int:pk2>', views.remove_shift_template,
    #      name='remove_shift_template'),
]
