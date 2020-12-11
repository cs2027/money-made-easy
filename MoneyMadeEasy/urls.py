from django.urls import path
from . import views

urlpatterns = [
    # Pages to view information (profile, current expenses, etc.)
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login_page", views.login_page, name="login"),
    path("logout_page", views.logout_page, name="logout"),
    path("expenses", views.expenses, name="expenses"),
    path("loan_calc", views.loan_calc, name="loan_calc"),
    path("loan_new", views.loan_new, name="loan_new"),
    path("loan_refinance", views.loan_refinance, name="loan_refinance"),
    path("visual", views.visual, name="visual"),

    # Pages to make edits (update profile, add new expenses, etc.)
    path("edit_profile", views.edit_profile, name="edit_profile"),
    path("add_expense", views.add_expense, name="add_expense"),
    path("edit_expense/<int:expense_ID>", views.edit_expense, name="edit_expense"),
    path("remove_expense/<int:expense_ID>", views.remove_expense, name="remove_expense")
]