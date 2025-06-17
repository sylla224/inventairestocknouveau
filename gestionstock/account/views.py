from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from account.forms import UserCreationForm, UserSearchForm, UserEditForm, UserPasswordChangeForm
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import CustomUser


# Create your views here.
def index(request):
    pass


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

    context = {
        'form': form,
        'search_form': search_form,
        'users': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
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
            return redirect('listes_users')
    
    return redirect('listes_users')

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
            return redirect('edit_user', user_id=user.id)
        else:
            messages.error(request, 'Please correct the password errors below.')
    
    return redirect('account:edit_user', user_id=user.id)
