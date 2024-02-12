from django.urls import path
from django.contrib import admin  # Import the admin module
from . import views  # Import the missing module
import django.views.static  # Import the missing module

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('<path:path>', django.views.static.serve),
]