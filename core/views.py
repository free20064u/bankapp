from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Customer, Account, Transaction
from .forms import CustomerForm, AccountForm

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a customer profile
            Customer.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    customer = request.user.customer
    accounts = customer.account_set.all()
    return render(request, 'profile.html', {'customer': customer, 'accounts': accounts})

@login_required
def edit_profile(request):
    customer = request.user.customer
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.customer = request.user.customer
            account.balance = 0
            account.save()
            return redirect('profile')
    else:
        form = AccountForm()
    return render(request, 'create_account.html', {'form': form})

@login_required
def view_transactions(request, account_id):
    account = get_object_or_404(Account, id=account_id, customer=request.user.customer)
    transactions = account.transaction_set.all().order_by('-timestamp')
    return render(request, 'view_transactions.html', {'account': account, 'transactions': transactions})
