from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('destination/<int:destination_id>', views.destination_detail, name='destination_detail'),
    path('activity/<int:activity_id>', views.activity_detail, name='activity_detail'),
    path('package/<int:package_id>', views.package_detail, name='package_detail'),
    path('book_activity/<int:package_id>/', views.book_activity, name='book_activity'),
    path('initkhalti', views.initkhalti, name='initkhalti'),
    path('return_url', views.return_url, name='return_url'),
    path('generate_uuid', views.generate_uuid, name='generate_uuid'),
    
]
