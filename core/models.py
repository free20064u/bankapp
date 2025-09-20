from django.db import models
from django.contrib.auth.models import User

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Account(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, default='EUR')

    def __str__(self):
        return self.account_number

    def deposit(self, amount, description="Deposit"):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.save()
        Transaction.objects.create(account=self, amount=amount, description=description)

    def withdraw(self, amount, description="Withdrawal"):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.balance < amount:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        self.save()
        Transaction.objects.create(account=self, amount=-amount, description=description)

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.account.account_number} - {self.amount}'