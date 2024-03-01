from django.shortcuts import render, get_object_or_404
from .models import Destination
# Create your views here.

def home(request,destination_id=None):
    destinations = Destination.objects.all()
    context = {
        'destinations': destinations
    }
    return render(request, "index.html", context)

def destination_detail(request, destination_id=None):
    destination = get_object_or_404(Destination, pk=destination_id)
    first_image_url = destination.images.first().image.url if destination.images.exists() else None
    destinations = Destination.objects.all()
    context = {
        'destination': destination,
        'destinations': destinations,
        'first_image_url': first_image_url,
    }
    return render(request, "destination.html", context)

