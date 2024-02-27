from django.shortcuts import render, get_object_or_404
from .models import Destination
# Create your views here.

def home(request):
    destinations = Destination.objects.all()
    context = {
        'destinations': destinations
    }
    return render(request, "index.html", context)

def destination_detail(request, destination_id=None):
    destination = get_object_or_404(Destination, pk=destination_id)
    context = {
        'destination': destination
    }
    return render(request, "destination.html", context)
