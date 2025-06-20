from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from account.forms import UserCreationForm, UserSearchForm, UserEditForm, UserPasswordChangeForm
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from account.forms import CustomUserCreationForm, EmailAuthenticationForm
from inventaire.models import Product, Enterprise, TypeEnterprise


# Create your views here.
def index(request):
    return render(request, 'account/dashboard.html')    


def listes_users(request):
    # Handle user creation
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.email} created successfully!')
            return redirect('manage_users')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()

    # Handle search
    search_form = UserSearchForm(request.GET)
    users = CustomUser.objects.all().order_by('-date_joined')

    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search')
        if search_query:
            users = users.filter(
                Q(email__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )

    # Pagination
    paginator = Paginator(users, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # number of users
    total_users = users.count()

    context = {
        'form': form,
        'search_form': search_form,
        'users': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'Users List':total_users
    }

    return render(request, 'account/listes.html', context)


def create_user(request):
    """Separate view for user creation (if needed)"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # check if the is gestionnaire field is checked and add the user to the gestionnaire group
            if form.cleaned_data.get('is_gestionnaire'):
                gestionnaire_group = request.user.groups.filter(name='gestionnaire')
                user = form.save()
                from django.contrib.auth.models import Group
                gestionnaire_group = Group.objects.get(name='gestionnaire')
                user.groups.add(gestionnaire_group)
                user.save()
            else:
                user = form.save()
                user = form.save()
            messages.success(request, f'User {user.email} created successfully!')
            return redirect('account:listes_users')
        else:
            messages.error(request, 'Please correct the errors below.')

    return redirect('account:listes_users')


def edit_user(request, pk):
    """View for editing user information"""
    user = get_object_or_404(CustomUser, id=pk)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, user=user)
        if form.is_valid():
            updated_user = form.save()
            messages.success(request, f'User {updated_user.email} updated successfully!')
            return redirect('account:edit_user', pk=user.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserEditForm(user=user)
    
    # Initialize password change form
    password_form = UserPasswordChangeForm(user=user)
    
    context = {
        'user': user,
        'form': form,
        'password_form': password_form,
    }
    
    return render(request, 'account/edit_user.html', context)


def delete_user(request, pk):
    """Handle user deletion"""
    user = get_object_or_404(CustomUser, id=pk)
    
    if request.method == 'POST':
        email = user.email
        user.delete()
        messages.success(request, f'User {email} deleted successfully!')
        
        # Check if we're coming from the edit page
        if 'edit_user' in request.META.get('HTTP_REFERER', ''):
            return redirect('account:listes_users')
    
    return redirect('account:listes_users')

def user_detail(request, pk):
    """View for displaying detailed user information"""
    user = get_object_or_404(CustomUser, id=pk)
    
    context = {
        'user': user,
    }
    
    return render(request, 'users/listes.html', context)

def change_user_password(request, pk):
    """View for changing user password"""
    user = get_object_or_404(CustomUser, id=pk)
    
    if request.method == 'POST':
        password_form = UserPasswordChangeForm(request.POST, user=user)
        if password_form.is_valid():
            password_form.save()
            messages.success(request, f'Password for {user.email} changed successfully!')
            return redirect('edit_user', pk=user.id)
        else:
            messages.error(request, 'Please correct the password errors below.')
    
    return redirect('account:edit_user', pk=user.id)

#User management views
User = get_user_model()
class CustomLoginView(LoginView):
    """Custom login view using email authentication"""
    form_class = EmailAuthenticationForm
    template_name = 'account/login.html'
    success_url = reverse_lazy('inventaire:dashboard')
    
    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().email}!')
        return super().form_valid(form)

# Custom logout view and closing the session
class CustomLogoutView(LogoutView):
    """Custom logout view"""
    next_page = reverse_lazy('account:login')
    print("je suis dans la vue de déconnexion")

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)
    
def home(request):
    """Home page view"""
    return render(request, 'home.html')

class SignUpView(CreateView):
    """User registration view"""
    model = User
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully! Please log in.')
        return response

def custom_login_redirect(request):
    """
    Custom view to redirect users based on their role after login
    """
    if request.user.is_authenticated:
        # Check if user has admin role (you can customize this logic)
        if request.user.groups.filter(name='administrator') :
            return redirect('account:admin_dashboard')
        elif request.user.groups.filter(name='gestionnaire'):
            return redirect('account:gestionnaire_dashboard')
        else:
            # Default redirect if role is not defined
            return redirect('account:dashboard')
    else:
        return redirect('account:login')

@login_required
def admin_dashboard(request):
    """
    Admin dashboard view
    """
    # Check if user is in the 'administrator' group
    if not request.user.groups.filter(name='administrator').exists():
        messages.error(request, "You don't have permission to access this page.")
        return redirect('account:gestionnaire_dashboard')
    # list of all users
    users = CustomUser.objects.all().order_by('-date_joined')
    # Total of products
    total_products = Product.objects.count()
    # Total of enterprises
    total_enterprises = Enterprise.objects.count()
    
    context = {
        'user_role': 'administrator',
        'dashboard_title': 'Administrator Dashboard',
        'total_users': users.count(),
        'total_products': total_products,
        'total_enterprises': total_enterprises,
    }
    return render(request, 'account/admin_dashbord.html', context)

@login_required
def gestionnaire_dashboard(request):
    """
    Gestionnaire dashboard view
    """
    # Check if user is in the 'gestionnaire' group
    if not request.user.groups.filter(name='gestionnaire').exists():
        messages.error(request, "You don't have permission to access this page.")
        return redirect('account:admin_dashboard')
    
    context = {
        'user_role': 'gestionnaire',
        'dashboard_title': 'Gestionnaire Dashboard'
    }
    return render(request, 'account/gestionnaire_dashboard.html', context)


