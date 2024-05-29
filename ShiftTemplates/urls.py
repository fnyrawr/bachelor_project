from django.urls import path
from . import views

urlpatterns = [
    # ShiftTemplates
    path('list/', views.shift_template_list, name='shift_templates'),
    path('create/', views.ShiftTemplateCreationView.as_view(), name='create_shift_template'),
    # path('show/<int:pk>', views.view_shift_template, name='view_shift_template'),
    path('edit/<int:pk>', views.edit_shift_template, name='edit_shift_template'),
    path('delete/<int:pk>', views.delete_shift_template, name='delete_shift_template'),
    # ShiftTemplatesQualifications
    path('show/<int:pk>/qualifications', views.get_qualifications, name='shift_template_qualifications'),
    path('show/<int:pk1>/add_qualification/<int:pk2>', views.add_qualification,
         name='add_shift_template_qualification'),
    path('show/<int:pk1>/remove_qualification/<int:pk2>', views.remove_qualification,
         name='remove_shift_template_qualification'),
]
