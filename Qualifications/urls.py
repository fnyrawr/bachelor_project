from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.qualification_list, name='qualifications'),
    path('create/', views.QualificationCreationView.as_view(), name='create_qualification'),
    path('show/<int:pk>', views.view_qualification, name='view_qualification'),
    path('edit/<int:pk>', views.edit_qualification, name='edit_qualification'),
    path('delete/<int:pk>', views.delete_qualification, name='delete_qualification'),
]