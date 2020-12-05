from django.contrib import admin
from .models import User, SimpleExpense, Loan

# Register your models here.
admin.site.register(User)
admin.site.register(SimpleExpense)
admin.site.register(Loan)
