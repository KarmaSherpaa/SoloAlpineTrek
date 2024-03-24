from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Destination , Activity , Package , Booking
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

from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Booking, Activity, Package, Destination

def book_activity(request, package_id):
    if request.method == 'POST':
        package = get_object_or_404(Package, pk=package_id)
        # activity= get_object_or_404(Activity, pk=activity_id)
        date = request.POST.get('date')
        # activity_id = request.POST.get('activity_id')  # Assuming activity_id is passed through the form
        if date:
  # Retrieve the activity associated with the package
            activity = package.activities

# Now that activity is defined, you can access its destination
            destination = activity.destination

            # Create a new booking record
            booking = Booking.objects.create(
                user=request.user,
                activity=activity,
                package=package,
                destination=destination,
                date_booked=date
            )
            messages.success(request, 'Booking successful!')
            return redirect('package_detail', package_id=package_id)
        else:
            messages.error(request, 'Please select a valid date and activity.')
            return redirect('package_detail', package_id=package_id)
    else:
        # If the request method is not POST, redirect to the package detail page
        return redirect('package_detail', package_id=package_id)