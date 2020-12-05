from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
from .models import User


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



