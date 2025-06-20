from django.urls import path, include
from account.views import listes_users, create_user, edit_user, delete_user, change_user_password, CustomLoginView, SignUpView, admin_dashboard, gestionnaire_dashboard, custom_login_redirect, index
from .views import  CustomLogoutView
app_name = 'account'

urlpatterns = [
    path('', custom_login_redirect, name='home'),
    path('users/listes', listes_users, name='listes_users'),
    path('users/create', create_user, name='create_user'),
    path('users/edit/<int:pk>/', edit_user, name='edit_user'),
    path('users/delete/<int:pk>/', delete_user, name='delete_user'),
    path('users/<int:pk>/change-password/', change_user_password, name='change_user_password'),
    path('users/<int:pk>/delete/', delete_user, name='delete_user'),
     # Authentication URLs - using custom login view
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLoginView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('gestionnaire/dashboard/', gestionnaire_dashboard, name='gestionnaire_dashboard'),
     path('dashboard', index, name='dashboard'),
]