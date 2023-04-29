from django.urls import path
from . import views

urlpatterns = [
    # Demand
    path('list/', views.demand_list, name='demand'),
    path('create/', views.DemandCreationView.as_view(), name='create_demand'),
    path('edit/<int:pk>', views.edit_demand, name='edit_demand'),
    path('delete/<int:pk>', views.delete_demand, name='delete_demand'),
]
