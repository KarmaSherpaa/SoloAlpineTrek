from django.urls import path
from . import views  # Import the missing module


urlpatterns = [
    path("about_us/", views.about_us, name="about_us"),
    path("Signin", views.signin, name="signin"),
    path("Signup", views.signup, name="signup"),
    path("Signout", views.signout, name="signout"),
    path("Profile", views.profile, name="profile"),
    path("EditProfile", views.edit_profile, name="edit_profile"),
    path('change_profile_pic', views.change_profile_pic , name='change_profile_pic'),
    path('update_password', views.update_password, name='update_password'),
    path('forget_Message', views.ForgetMessage, name='forget_Message'),
    path('forget-password/' , views.ForgetPassword , name="forget_password"),
    path('change-password/<token>/' , views.ChangePassword , name="change_password"),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('bookings/', views.bookings, name='bookings'),
    path('update_booking/', views.update_booking, name='update_booking'),
    path('booking_updates/<int:booking_id>/', views.booking_updates, name='booking_updates'),
    path('inquiry/', views.inquiry, name='inquiry'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('submit_inquiry/', views.submit_inquiry, name='submit_inquiry'),
    path('feedback/', views.feedback, name='feedback'),
    path('submit_feedback/', views.submit_feedback, name='submit_feedback'),
]


