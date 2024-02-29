from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('destination/', views.destination_detail, name='destination_details'),  # Remove the trailing slash
    path('destination/<int:destination_id>/', views.destination_detail, name='destination_detail'),
]
