from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Customer, Account, Transaction
from .forms import AccountForm, TransactionForm
from django.db.models import Sum # Import Sum for aggregation

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')

@login_required
def dashboard(request):
    customer, created = Customer.objects.get_or_create(user=request.user)
    accounts = customer.account_set.all()
    total_balance = accounts.aggregate(Sum('balance'))['balance__sum'] or 0.00
    recent_transactions = Transaction.objects.filter(account__customer=customer).order_by('-timestamp')[:5]

    context = {
        'customer': customer,
        'accounts': accounts,
        'total_balance': total_balance,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'dashboard.html', context)

@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.customer = request.user.customer
            account.balance = 0
            account.save()
            messages.success(request, "Account created successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Error creating account. Please check the form.")
    else:
        form = AccountForm()
    return render(request, 'create_account.html', {'form': form})

@login_required
def view_transactions(request, account_id):
    account = get_object_or_404(Account, id=account_id, customer=request.user.customer)
    transactions = account.transaction_set.all().order_by('-timestamp')
    return render(request, 'view_transactions.html', {'account': account, 'transactions': transactions})

@login_required
def make_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user) # Pass user to form
        if form.is_valid():
            account = form.cleaned_data['account']
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            transaction_type = form.cleaned_data['transaction_type']
            recipient_account = form.cleaned_data.get('recipient_account') # Get recipient account

            # Ensure the source account belongs to the current user
            if account.customer != request.user.customer:
                messages.error(request, "You can only make transactions from your own accounts.")
            else:
                try:
                    if transaction_type == 'deposit':
                        account.deposit(amount, description)
                        messages.success(request, "Deposit successful!")
                    elif transaction_type == 'withdrawal':
                        account.withdraw(amount, description)
                        messages.success(request, "Withdrawal successful!")
                    elif transaction_type == 'transfer':
                        if not recipient_account:
                            messages.error(request, "Recipient account is required for transfers.")
                        elif account.currency != recipient_account.currency:
                            messages.error(request, "Cannot transfer between accounts of different currencies.")
                        elif account == recipient_account:
                            messages.error(request, "Cannot transfer to the same account.")
                        else:
                            # Perform withdrawal from sender
                            account.withdraw(amount, f"Transfer to {recipient_account.account_number}: {description}")
                            # Perform deposit to recipient
                            recipient_account.deposit(amount, f"Transfer from {account.account_number}: {description}")
                            messages.success(request, f"Transfer of {amount} from {account.account_number} to {recipient_account.account_number} successful!")
                    return redirect('accounts:profile')
                except ValueError as e:
                    messages.error(request, str(e))
        else:
            messages.error(request, "Error processing transaction. Please check the form.")
    else:
        form = TransactionForm(user=request.user) # Pass user to form
    return render(request, 'make_transaction.html', {'form': form})

def about(request):
    return render(request, 'about.html')