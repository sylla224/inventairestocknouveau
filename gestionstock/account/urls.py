from django.urls import path, include
from .views import listes_users, create_user, edit_user, delete_user, change_user_password
app_name = 'account'

urlpatterns = [
    path('users/listes', listes_users, name='listes_users'),
    path('users/create', create_user, name='create_user'),
    path('users/edit/<int:pk>/', edit_user, name='edit_user'),
    path('users/delete/<int:pk>/', delete_user, name='delete_user'),
    path('users/<int:user_id>/change-password/', change_user_password, name='change_user_password'),
    path('users/<int:user_id>/delete/', delete_user, name='delete_user'),
]