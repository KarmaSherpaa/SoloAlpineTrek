from django.db.models import Q
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import User 
from home.models import Destination
from django.contrib.auth import authenticate, login

# check if string is email
def is_email(string):
    if '@' in string:
        return True 
    return False

def signup(request):
    destinations = Destination.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')  # Retrieve username from form
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        dob = request.POST.get('dob')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            context = {
                "username": username,
                "full_name": full_name,
                "email": email,
                "dob": dob,
                "address": address,
                "contact": contact,
                "password": password,
                "confirm_password": confirm_password,
            }
            return render(request, 'Signup.html', context=context)

        if password == confirm_password:
            user = User.objects.create_user(username=username, full_name=full_name, dob=dob, email=email, address=address, contact=contact)
            user.set_password(password)
            user.save()
            messages.success(request, 'Registration Successful')
            return redirect('/Signin')
  
    return render(request, 'Signup.html' , {'destinations': destinations})


def signin(request):
    destinations = Destination.objects.all()
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')

        # Query users by username or email using Q objects
        user = User.objects.filter(Q(username=username_or_email) | Q(email=username_or_email)).first()

        if user is not None:
            authenticated_user = authenticate(username=user.username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid Password')
        else:
            messages.error(request, 'Invalid Username or Email')

    return render(request, 'Signin.html', {'destinations': destinations})

def signout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('/')