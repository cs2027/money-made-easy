from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
from .models import User, Expense


# Initial landing page for users (displays basic profile info)
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


# View all monthly expenses
def expenses(request):
    expenses = request.user.expenses.all()
    return render(request, "MoneyMadeEasy/expenses.html", {
        "expenses": expenses
    })


# Links to loan-related calculations
def loan_calc(request):
    return render(request, "MoneyMadeEasy/loan_calc.html")


# Calculate payments on a new loan
def loan_new(request):
    return render(request, "MoneyMadeEasy/loan_new.html")


# Calculate adjusted payments after refinancing an existing loan
def loan_refinance(request):
    return render(request, "MoneyMadeEasy/loan_refinance.html")


# Visual representation of monthly expenses
def visual(request):
    # Parse current user data (income, savings goal, expenses)
    expenses = request.user.expenses.all()
    amounts = []

    for expense in expenses:
        amounts.append(float(expense.amount))

    total_DI = request.user.monthly_DI
    savings = request.user.goal_savings

    # If data is unsufficient (no income/savings info, no expenses), render an alternate template
    if total_DI == 0 or savings == 0 or len(amounts) == 0:
        return render(request, "MoneyMadeEasy/visual_error.html")

    avg = sum(amounts) / len(amounts) 
    remainder = total_DI - savings - request.user.total_expenses 

    # Else, dispatch based on whether or not the user is over budget
    if remainder >= 0:
        return render(request, "MoneyMadeEasy/visual.html", {
            "expenses": expenses,
            "amounts": amounts,
            "avg": avg,
            "total_DI": total_DI,
            "remainder": remainder,
            "savings": savings, 
            "over_budget": False
        })
 
    return render(request, "MoneyMadeEasy/visual.html", {
        "expenses": expenses,
        "amounts": amounts,
        "avg": avg,
        "total_DI": total_DI,
        "remainder": abs(remainder),
        "savings": savings,
        "over_budget": True
    })


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

        # Return to main landing page
        return HttpResponseRedirect(reverse("index"))

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

        # Error catching in case of invalid inputs
        if name.strip() == "":
            return render(request, "MoneyMadeEasy/add_expense.html", {
                "message": "Error: You cannot have a blank name."
            })
        elif category == "None":
            return render(request, "MoneyMadeEasy/add_expense.html", {
                "message": "Error: You must select an expense category."
            })


        # Create and save the new expense object to the database
        new_expense = Expense.objects.create(name=name, category=category, amount=amount, belongs_to=user)
        new_expense.save()

        # Update the user's profile (total monthly expenses)
        update_expenses(user)

        # Display all of the user's expenses (including the new one)
        return HttpResponseRedirect(reverse("expenses"))

    # For a 'GET' request, display the form to add a new expense
    return render(request, "MoneyMadeEasy/add_expense.html")


# Edit an existing expense
def edit_expense(request, expense_ID):
    # Obtain the desired expense object
    expense = Expense.objects.get(id=expense_ID)

    # Go here for 'POST' requests
    if request.method == "POST":
        # Obtain relevant info about current user & expense
        user_ID = int(request.POST["user_ID"])
        user = User.objects.get(id=user_ID)
        name = request.POST["name"]
        category = request.POST["category"]
        amount = request.POST["amount"]

        # Error catching in case of invalid inputs
        if name.strip() == "":
            return render(request, "MoneyMadeEasy/edit_expense.html", {
                "expense": expense,
                "message": "Error: You cannot have a blank name."
            })
        elif category == "None":
            return render(request, "MoneyMadeEasy/edit_expense.html", {
                "expense": expense,
                "message": "Error: You must select an expense category."
            })

        # Update the desired expense object
        expense.name = name
        expense.category = category
        expense.amount = amount
        expense.save()

        # Update the user's profile (total expenses) & reload updated list of expenses
        update_expenses(user)
        return HttpResponseRedirect(reverse("expenses"))

    # For a 'GET' request, display the form to edit an existing expense
    return render(request, "MoneyMadeEasy/edit_expense.html", {
        "expense": expense
    })


# Remove a given `expense` object from the database
def remove_expense(request, expense_ID):
    expense = Expense.objects.get(id=expense_ID)
    expense.delete()
    
    update_expenses(request.user)
    return HttpResponseRedirect(reverse("expenses"))


# Helper function to update a user's total monthly expenses
def update_expenses(user):
    expenses = user.expenses.all()
    total_expenses = 0

    for expense in expenses:
        total_expenses += expense.amount
    
    user.total_expenses = total_expenses
    user.save()