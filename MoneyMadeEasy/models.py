from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User model
class User(AbstractUser):
    monthly_DI = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    goal_savings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

# TODO
class Expense(models.Model):
    name = models.CharField(max_length=128)
    category = models.CharField(max_length=64)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    belongs_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    outstanding = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    int_rate = models.DecimalField(max_digits=4, decimal_places=2, blank=True)
    term_len = models.DecimalField(max_digits=4, decimal_places=2, blank=True)

    def __str__(self):
        return f"{self.name}: ${self.amount}/month ({self.belongs_to.username})"


    