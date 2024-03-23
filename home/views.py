from django.shortcuts import render, get_object_or_404
from .models import Destination , Activity , Package
# Create your views here.

def home(request):
    destinations = Destination.objects.all()
    
    # Get the currently logged-in user's name if available
    user_name = None
    if request.user.is_authenticated:
        user_name = request.user.username

    context = {
        'destinations': destinations,
        'user_name': user_name  # Include the user's name in the context
    }
    return render(request, "index.html", context)


def destination_detail(request, destination_id=None):
    destination = get_object_or_404(Destination, pk=destination_id)
    first_image_url = destination.images.first().image.url if destination.images.exists() else None
    destinations = Destination.objects.all()
    activities = destination.activity_set.all()
    context = {
        'destination': destination,
        'destinations': destinations,
        'first_image_url': first_image_url,
        'activities': activities
    }
    return render(request, "destination.html", context)

def activity_detail(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    destinations = Destination.objects.all()
    packages = Package.objects.filter(activities=activity)
    return render(request, 'activity.html', {'activity': activity , 'packages': packages,'destinations': destinations,})

def package_detail(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    destinations = Destination.objects.all()
    return render(request, 'packages.html', {'package': package, 'destinations': destinations,})

