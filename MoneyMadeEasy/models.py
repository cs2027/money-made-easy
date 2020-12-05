from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User model
class User(AbstractUser):
    monthly_DI = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    goal_savings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

# Fixed/recurring expenses (insurance, utility bills, groceries, etc.)
class SimpleExpense(models.Model):
    name = models.CharField(max_length=128)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    belongs_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="simple_expenses")

# Payments related to loans (mortages, student loans, etc.)
class Loan(models.Model):
    name = models.CharField(max_length=128)
    outstanding = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    int_rate = models.DecimalField(max_digits=4, decimal_places=2, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    belongs_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans")