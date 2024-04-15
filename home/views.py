from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Destination , Activity , Package , Booking
import json
import requests
import uuid
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
    
    uuid_val = uuid.uuid4()
    return render(request, 'packages.html', {'package': package, 'destinations': destinations, 'uuid_val': uuid_val, })

from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Booking, Activity, Package, Destination

def book_activity(request, package_id):

    print("yoyo")

    uuid_val = uuid.uuid4()
    print(uuid_val)

    if request.method == 'POST':
        package = get_object_or_404(Package, pk=package_id)
        print("yyoyo")
        # activity= get_object_or_404(Activity, pk=activity_id)
        date = request.POST.get('date')
        # activity_id = request.POST.get('activity_id')  # Assuming activity_id is passed through the form
        participants = request.POST.get('participants')
        special_requirements = request.POST.get('special_requirements')
        if date  and participants:
            activity = package.activities

            destination = activity.destination

            # Create a new booking record
            booking = Booking.objects.create(
                user=request.user,
                activity=activity,
                package=package,
                destination=destination,
                date_booked=date,
                participants=participants,
                special_requirements=special_requirements
            )
            messages.success(request, 'Booking successful!')
            print("I m" ,uuid_val)
            return redirect('package_detail', package_id=package_id)
        else:
            messages.error(request, 'Please select a valid date and  specify the number of participants.')
            return redirect('package_detail', package_id=package_id)

def generate_uuid(request):
    uuid_val = uuid.uuid4()
    print(uuid_val)
    context = {
        'uuid_val': uuid_val,
    }
    return render(request, 'packages.html',context)

def initkhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    user= request.user

    return_url = request.POST.get('return_url')
    amount = request.POST.get('amount')
    purchase_order_id = request.POST.get('purchase_order_id')
    print(return_url, amount, purchase_order_id)

    payload = json.dumps({
        "return_url": return_url,
        "website_url": "http://127.0.0.1:8000/",
        "amount": amount,
        "purchase_order_id": purchase_order_id,
        "purchase_order_name": "test",
        "customer_info": {
        "name": user.full_name,
        "email": user.email,
        "phone": user.contact
        }
    })

    # put your own live secet for admin
    headers = {
        'Authorization': 'key 99c941f5faf74fd2939cc9290c068d83',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(json.loads(response.text))

    print(response.text)
    new_res = json.loads(response.text)
    # print(new_res['payment_url'])
    print(type(new_res))
    return redirect(new_res['payment_url'])

def return_url(request):
    return render(request, 'index.html')
    # url = "https://a.khalti.com/api/v2/epayment/lookup/"
    # if request.method == 'GET':
    #     headers = {
    #         'Authorization': 'key b885cd9d8dc04eebb59e6f12190ae017',
    #         'Content-Type': 'application/json',
    #     }
    #     pidx = request.GET.get('pidx')
    #     data = json.dumps({
    #         'pidx':pidx
    #     })
    #     res = requests.request('POST',url,headers=headers,data=data)
    #     print(res)
    #     print(res.text)

    #     new_res = json.loads(res.text)
    #     print(new_res)
        

    #     if new_res['status'] == 'Completed':
    #         # user = request.user
    #         # user.has_verified_dairy = True
    #         # user.save()
    #         # perform your db interaction logic
    #         pass
        
        # else:
        #     # give user a proper error message
        #     raise BadRequest("sorry ")

        # return redirect('home')
    
