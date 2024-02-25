from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # path("about/", views.about, name="Aboutus"),
    # path("contact/", views.contact, name="Contact"),
    # path("blog/", views.blog, name="Blog"),
    # path("gallery/", views.gallery, name="Gallery"),
    # path("services/", views.services, name="Services"),
     path("destination", views.destination, name="destination"),
]   