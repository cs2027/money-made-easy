from django.urls import path
from . import views

urlpatterns = [
    # TODO
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login_page", views.login_page, name="login"),
    path("logout_page", views.logout_page, name="logout"),
    path("profile", views.profile, name="profile"),
    path("expenses", views.expenses, name="expenses"),
    path("loan_calc", views.loan_calc, name="loan_calc"),
    path("loan_new", views.loan_new, name="loan_new"),
    path("loan_refinance", views.loan_refinance, name="loan_refinance"),
    path("visual", views.visual, name="visual"),

    # TODO
]