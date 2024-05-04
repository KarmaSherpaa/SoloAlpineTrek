from django.urls import path
from . import views  # Import the missing module


urlpatterns = [
    path("Signin", views.signin, name="signin"),
    path("Signup", views.signup, name="signup"),
    path("Signout", views.signout, name="signout"),
    path("Profile", views.profile, name="profile"),
    path("EditProfile", views.edit_profile, name="edit_profile"),
    path('change_profile_pic', views.change_profile_pic , name='change_profile_pic'),
]