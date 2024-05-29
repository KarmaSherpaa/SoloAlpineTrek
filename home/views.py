from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Destination , Activity , Package , Booking
import json
import requests
import uuid
from django.contrib.auth.decorators import login_required
from datetime import datetime
from accounts.models import feedback
from django.db.models import Count
from random import randint
# Create your views here.

def home(request):
    destinations = Destination.objects.all()
    count = feedback.objects.aggregate(count=Count('id'))['count']
    random_index = randint(0, count - 3)
    feedbacks = feedback.objects.all()[random_index:random_index + 3]
    
    # Get the currently logged-in user's name if available
    user_name = None
    recent_booking = None
    if request.user.is_authenticated:
        user_name = request.user.username
       

    # Get the most booked package
    packages = Package.objects.annotate(num_bookings=Count('booking')).order_by('-num_bookings')[:6]

    context = {
        'destinations': destinations,
        'feedbacks': feedbacks,
        'user_name': user_name,  # Include the user's name in the context
        'packages': packages,
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

@login_required
def book_activity(request, package_id):
    uuid_val = uuid.uuid4()
    if request.method == 'POST':
        if Booking.objects.filter(package_id=package_id, user=request.user).exists():
            messages.error(request, 'You have already booked this package.')
            return redirect('package_detail', package_id=package_id)
        package = get_object_or_404(Package, pk=package_id)
        # activity= get_object_or_404(Activity, pk=activity_id)
        date_str = request.POST.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        date = request.POST.get('date')
        print(date)  
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
                date=date,
                participants=participants,
                special_requirements=special_requirements,
                payment_gateway=False  # Set to False for bookings without payment gateway
            )
            messages.success(request, 'Booking successful!')
            return redirect('/', package_id=package_id)
        else:
            messages.error(request, 'Please select a valid date and  specify the number of participants.')
            return redirect('package_detail', package_id=package_id)

def generate_uuid(request):
    uuid_val = uuid.uuid4()
    context = {
        'uuid_val': uuid_val,
    }
    return render(request, 'packages.html',context)

@login_required
def initkhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    user= request.user
    return_url = request.POST.get('return_url')
    amount = request.POST.get('amount')
    purchase_order_id = request.POST.get('purchase_order_id')
    date = request.POST.get('date')
    participants = request.POST.get('participants')
    special_requirements = request.POST.get('special_requirements')
  
    request.session['date'] = date
    request.session['participants'] = participants
    request.session['special_requirements'] = special_requirements
    payload = json.dumps({
        "return_url": return_url,
        "website_url": "http://127.0.0.1:8000/",
        "amount": amount,
        "purchase_order_id": purchase_order_id,
        "purchase_order_name": "test",
        "customer_info": {
        "name": user.full_name,
        "email": user.email,
        "phone": user.contact,
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

@login_required
def return_url(request, package_id):
    if request.method == 'GET':
        if Booking.objects.filter(package_id=package_id, user=request.user).exists():
            messages.error(request, 'You have already booked this package.')
            return redirect('package_detail', package_id=package_id)
        print(request.GET) 
        package = get_object_or_404(Package, pk=package_id)
        date = request.session.get('date')
        participants = request.session.get('participants')
        special_requirements = request.session.get('special_requirements')
        print(f'Participants: {participants}, Special Requirements: {special_requirements}')  # Debug line
        pidx = request.GET.get('pidx')

        url = "https://a.khalti.com/api/v2/epayment/lookup/"
        headers = {
            'Authorization': 'key 99c941f5faf74fd2939cc9290c068d83',
            'Content-Type': 'application/json',
        }
        data = json.dumps({
            'pidx': pidx,
            "participants":participants,
            "special_requirements":special_requirements,
        })
        res = requests.post(url, headers=headers, data=data)
        new_res = res.json()

        if new_res.get('status') == 'Completed':
            activity = package.activities
            destination = activity.destination

            # Create a new booking record
            booking = Booking.objects.create(
                user=request.user,
                activity=activity,
                package=package,
                destination=destination,
                date=date,
                participants=participants,
                special_requirements=special_requirements,
                pidx=new_res.get('pidx'),
                status=new_res.get('status'),
                transection_id=new_res.get('transaction_id'),
                fee=new_res.get('fee'),
                refunded=new_res.get('refunded'),
                payment_gateway=True,
                price=package.price,
            )
            messages.success(request, 'Booking successful!')
            return redirect('/', package_id=package_id)
        else:
            messages.error(request, 'Payment was not successful. Please try again.')
            return redirect('package_detail', package_id=package_id)
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('package_detail', package_id=package_id)
    
from django.http import JsonResponse

def check_booking(request, package_id):
    if request.user.is_authenticated:
        already_booked = Booking.objects.filter(package_id=package_id, user=request.user).exists()
        return JsonResponse({'already_booked': already_booked})
    else:
        return JsonResponse({'already_booked': False})
 