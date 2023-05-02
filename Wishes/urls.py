from django.urls import path
from . import views

urlpatterns = [
    # Wishes
    path('list/', views.wish_list, name='wishes'),
    path('create/', views.WishCreationView.as_view(), name='create_wish'),
    path('edit/<int:pk>', views.edit_wish, name='edit_wish'),
    path('delete/<int:pk>', views.delete_wish, name='delete_wish'),
    path('list-own', views.own_wishes, name='own_wishes'),
    path('add-own', views.OwnWishCreationView.as_view(), name='add_own_wish'),
    path('edit-own/<int:pk>', views.edit_own_wish, name='edit_own_wish'),
    path('delete-own/<int:pk>', views.delete_own_wish, name='delete_own_wish'),
]
