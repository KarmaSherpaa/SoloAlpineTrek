from django.urls import path
from django.contrib import admin  # Import the admin module
from . import views  # Import the missing module
import django.views.static  # Import the missing module

urlpatterns = [
    path("Signin", views.signin, name="signin"),
    path("Signup", views.signup, name="signup")
]