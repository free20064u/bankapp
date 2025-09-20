from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from core.models import Customer, Account # Import Customer and Account from core
from .forms import CustomerForm # Import CustomerForm from accounts.forms

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a customer profile
            Customer.objects.create(user=user)
            login(request, user)
            return redirect('dashboard') # Redirect to dashboard after registration
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard') # Redirect to dashboard after login
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home') # Redirect to home after logout

@login_required
def profile(request):
    customer, created = Customer.objects.get_or_create(user=request.user)
    # accounts = customer.account_set.all() # Accounts are handled in core app
    return render(request, 'accounts/profile.html', {'customer': customer}) # Removed accounts from context

@login_required
def edit_profile(request):
    customer = request.user.customer
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('accounts:profile') # Redirect to accounts:profile
        else:
            messages.error(request, "Error updating profile. Please check the form.")
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'accounts/edit_profile.html', {'form': form})