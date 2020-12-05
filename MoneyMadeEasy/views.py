from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
from .models import User, Expense


# Initial landing page for users
def index(request):
    # Display landing page for authenticated users
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    # Else, direct the user to the login page
    return render(request, "MoneyMadeEasy/index.html")


# Page to register a new user
def register(request):
    if request.method == "POST":
        # Parse new user information
        username = str(request.POST["username"])
        password = str(request.POST["password"])
        password_confirm = str(request.POST["password_confirm"])

        # Error catching (blank fields, passwords don't match)
        if username.replace(' ', '') == "":
            return render(request, "MoneyMadeEasy/register.html", {
                "message": "You cannot have a blank username."
            })
        elif password.replace(' ', '') == "":
            return render(request, "MoneyMadeEasy/register.html", {
                "message": "You cannot have a blank password."
            })
        elif not password == password_confirm:
            return render(request, "MoneyMadeEasy/register.html", {
                "message": "Your passwords do not match."
            })

        # Attempt to create a new user
        try:
            new_user = User.objects.create_user(username, None, password)
            new_user.save()
        except IntegrityError:
            return render(request, "MoneyMadeEasy/register.html", {
                "message": "Sorry! That username is already taken."
            })

        # Login the new user & redirect him/her to the index page
        login(request, new_user)
        return HttpResponseRedirect(reverse("index"))

    # For a 'GET' request, simply display the registration form
    return render(request, "MoneyMadeEasy/register.html")


# Page to login to user account
def login_page(request):
    if request.method == "POST":
        # Parse user inputs for username & password
        username = request.POST["username"]
        password = request.POST["password"]

        # Attempt to authenticate the user 
        user = authenticate(request, username=username, password=password)

        # Direct user to index page only if authentication succeeded
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "MoneyMadeEasy/login.html", {
                "message": "Invalid Login Credentials"
            })
    
    # For a 'GET' request, simply display the login page
    return render(request, "MoneyMadeEasy/login.html")


# Page displayed after a user logs out
def logout_page(request):
    # Direct the user back to the initial login page
    logout(request)
    return render(request, "MoneyMadeEasy/login.html", {
        "message": "You have now logged out."
    })


# Display profile info associated with current user
def profile(request):
    return render(request, "MoneyMadeEasy/profile.html")


# TODO
def expenses(request):
    # TODO
    expenses = request.user.expenses.all()
    return render(request, "MoneyMadeEasy/expenses.html", {
        "expenses": expenses
    })


# TODO
def loan_calc(request):
    return render(request, "MoneyMadeEasy/loan_calc.html")


# TODO
def loan_new(request):
    return render(request, "MoneyMadeEasy/loan_new.html")


# TODO
def loan_refinance(request):
    return render(request, "MoneyMadeEasy/loan_refinance.html")


# TODO
def visual(request):
    return render(request, "MoneyMadeEasy/visual.html")


# Edit current user's profile info
def edit_profile(request):
    if request.method == "POST":
        # Parse form fields/data
        user_ID = int(request.POST["user_ID"])
        user = User.objects.get(id=user_ID)
        new_DI = request.POST["new_DI"]
        new_GS = request.POST["new_GS"]

        # Update monthly disposable income and goal savings
        user.monthly_DI = new_DI
        user.goal_savings = new_GS
        user.save()

        # Return to profile page
        return HttpResponseRedirect(reverse("profile"))

    # For a 'GET' request, display the "edit profile" page
    return render(request, "MoneyMadeEasy/edit_profile.html")


# Add new monthly expenses (both loans & fixed costs)
def add_expense(request):
    if request.method == "POST":
        # Parse data regarding the new expense
        user_ID = int(request.POST["user_ID"])
        user = User.objects.get(id=user_ID)
        name = request.POST["name"]
        category = request.POST["category"]
        amount = request.POST["amount"]
        outstanding = 0
        int_rate = 0
        term_len = 0

        # Parse optional data if the expense was a loan
        if not request.POST["outstanding"]:
            pass
        else:
            outstanding = request.POST["outstanding"]

        if not request.POST["int_rate"]:
            pass
        else:
            int_rate = request.POST["int_rate"]

        if not request.POST["term_len"]:
            pass
        else:
            term_len = request.POST["term_len"]

        # Create and save the new expense object to the database
        new_expense = Expense.objects.create(name=name, category=category, amount=amount, belongs_to=user, outstanding=outstanding, int_rate=int_rate, term_len=term_len)
        new_expense.save()

        # Update the user's profile (total monthly expenses)
        expenses = user.expenses.all()
        total_expenses = 0

        for expense in expenses:
            total_expenses += expense.amount
        
        user.total_expenses = total_expenses
        user.save()

        # Display all of the user's expenses (including the new one)
        return HttpResponseRedirect(reverse("expenses"))

    # For a 'GET' request, display the form to add a new expense
    return render(request, "MoneyMadeEasy/add_expense.html")

