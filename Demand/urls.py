from django.urls import path
from . import views

urlpatterns = [
    # Demand
    path('list/', views.demand_list, name='demand'),
    path('create/', views.DemandCreationView.as_view(), name='create_demand'),
    # path('show/<int:pk>', views.view_demand, name='view_demand'),
    # path('edit/<int:pk>', views.edit_department, name='edit_demand'),
    # path('delete/<int:pk>', views.delete_department, name='delete_demand'),
]
