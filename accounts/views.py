import uuid
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Inquiry, User, Profile
from home.models import Booking, Destination 
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .helpers import send_forget_password_mail
from django.core.exceptions import ValidationError
from .forms import  FeedbackForm, InquiryForm, ProfileImageForm
from .models import UserProfile
from datetime import datetime
from dateutil.relativedelta import relativedelta


# check if string is email
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        dob = request.POST.get('dob')
        try:
            dob = datetime.strptime(dob, "%Y-%m-%d")  # assuming dob is in format 'YYYY-MM-DD'
        except ValueError:
            messages.error(request, 'Invalid date format. Expected YYYY-MM-DD.')
            return render(request, 'Signup.html')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if dob > datetime.now() - relativedelta(years=18):
            messages.error(request, 'You must be at least 18 years old to register.')
            return render(request, 'Signup.html')
        # Check if passwords match
        if len(password) < 8 or not any(char.islower() for char in password) or not any(char.isupper() for char in password) or not any(char.isdigit() for char in password):
            messages.error(request, 'Password must contain at least 8 characters, at least one uppercase letter, at least one lowercase letter, and at least one number.')
            return render(request, 'Signup.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'Signup.html')
        # Check if username already exists
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

        # Validate contact number
        try:
            user = User(username=username, email=email, full_name=full_name, contact=contact, address=address, dob=dob)
            user.set_password(password)
            user.full_clean()  # This will validate the model fields
            user.save()

            # Create user profile
            UserProfile.objects.create(user=user)

            messages.success(request, 'Registration Successful')
            return redirect('/Signin')
        except ValidationError as e:
            for field, error in e.message_dict.items():
                messages.error(request, f"{field}: {error[0]}")

    return render(request, 'Signup.html')


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
                messages.success(request, 'You have successfully logged in.')
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

@login_required
def profile(request):
    user = request.user
    context = {
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email,
        "dob": user.dob.strftime('%Y-%m-%d') if user.dob else '',
        "address": user.address,
        "contact": user.contact,
    }
    return render(request, 'users-profile.html', context=context)

@login_required
def edit_profile(request):
    user = request.user
    
    if request.method == 'POST':
        # Fetch form data, defaulting to existing values if not provided
        username = request.POST.get('username', user.username)
        full_name = request.POST.get('full_name', user.full_name)
        email = request.POST.get('email', user.email)
        contact = request.POST.get('contact', user.contact)
        address = request.POST.get('address', user.address)
        dob_str = request.POST.get('dob', user.dob.strftime('%Y-%m-%d') if user.dob else '')

        # Handle Date of Birth
        if dob_str:
            try:
                dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
                if dob > datetime.now().date():
                    raise ValidationError('Date of Birth cannot be in the future.')
            except ValueError:
                messages.error(request, 'Invalid Date Format. Please use " "Y-m-d"" format.')
                return render(request, 'users-profile.html', {
                    "username": username,
                    "full_name": full_name,
                    "email": email,
                    "dob": dob_str,
                    "address": address,
                    "contact": contact,
                })
            except ValidationError as e:
                messages.error(request, str(e))
                return render(request, 'users-profile.html', {
                    "username": username,
                    "full_name": full_name,
                    "email": email,
                    "dob": dob_str,
                    "address": address,
                    "contact": contact,
                })
        else:
            dob = user.dob

        # Validate contact number length
        if contact and (len(contact) != 10 or not contact.isdigit()):
            messages.error(request, 'Contact number must be exactly 10 digits.')
            return render(request, 'users-profile.html', {
                "username": username,
                "full_name": full_name,
                "email": email,
                "dob": dob_str,
                "address": address,
                "contact": contact,
            })

        # Update user fields
        user.username = username
        user.full_name = full_name
        user.email = email
        user.contact = contact
        user.address = address
        user.dob = dob

        try:
            user.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('/Profile')
        except Exception as e:
            messages.error(request, f'Error updating profile: {e}')

    return render(request, 'users-profile.html', {
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email,
        "dob": user.dob.strftime('%Y-%m-%d') if user.dob else '',
        "address": user.address,
        "contact": user.contact,
    })


@login_required
def change_profile_pic(request):
    if request.method == "POST":
        user_profile = request.user.userprofile
        form = ProfileImageForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            user_profile.save()
            messages.success(request, 'Profile picture changed successfully.')
    return redirect('profile')

from django.contrib.auth import update_session_auth_hash

@login_required
def update_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('password')
        new_password = request.POST.get('newpassword')
        confirm_password = request.POST.get('renewpassword')
        user = request.user
        if not user.check_password(old_password):
            messages.error(request, 'Invalid old password')
        elif new_password != confirm_password:
            messages.error(request, 'Passwords do not match')
        elif len(new_password) < 8 or not any(char.islower() for char in new_password) or not any(char.isupper() for char in new_password) or not any(char.isdigit() for char in new_password):
            messages.error(request, 'Password must contain at least 8 characters, at least one uppercase letter, at least one lowercase letter, and at least one number.')
        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # This will update the session and keep the user logged in.
            messages.success(request, 'Password changed successfully')
    return redirect('profile')


def ForgetPassword(request):
        if request.method == 'POST':
            email = request.POST.get('email')
            
            if not User.objects.filter(email=email).exists():
                messages.error(request, 'No user found with this username.')
                return redirect('/forget-password/')
            else:
                user_obj = User.objects.get(email=email)
                token = str(uuid.uuid4())
                profile_obj, created = Profile.objects.get_or_create(user=user_obj)
                print("yaha samma aayo hai")
                profile_obj.forget_password_token = token
                profile_obj.save()
                send_forget_password_mail(user_obj.email, token)
                return redirect('forget_Message')

        return render(request, 'forget-password.html')

def ForgetMessage(request):
    return render(request, 'forget-message.html')

def ChangePassword(request, token):
    try:
        profile_obj = Profile.objects.get(forget_password_token=token)
        user = profile_obj.user
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'change-password.html', {'token': token})
            user.set_password(new_password)
            user.save()
            
            # Clear forget password token
            profile_obj.forget_password_token = ''
            profile_obj.save()
            
            messages.success(request, 'Password changed successfully. Please login with your new password.')
            return redirect('/Signin')
    except Profile.DoesNotExist:
        messages.error(request, 'Invalid token.')
        return redirect('/forget-password/')
    except Exception as e:
        messages.error(request, 'An error occurred.')
        print(e)
    
    return render(request, 'change-password.html', {'token': token})
def bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings.html', {'bookings': bookings})

def update_booking(request):
    return render(request, 'update_booking.html')

def booking_updates(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        date_str = request.POST.get('date')
        participants = request.POST.get('participants')
        special_requirements = request.POST.get('special_requirements')

        if date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            if date <= datetime.now().date():
                messages.error(request, 'Booking date should be a future date.')
                return render(request, 'update_booking.html', {'booking': booking})
            booking.date_booked = date
        if participants:
            booking.participants = participants
        if special_requirements:
            booking.special_requirements = special_requirements


        booking.save()
        messages.success(request, 'Booking updated successfully.')
        return redirect('bookings')

    return render(request, 'update_booking.html', {'booking': booking})
    
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.user == booking.user:  # Ensure the user is authorized to cancel this booking
        booking.delete()
        messages.success(request, 'Booking cancelled successfully.')
    return redirect('bookings')

# def inquery(request):
#     return render(request, 'inquery.html')

@login_required
def submit_inquiry(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.user = request.user
            inquiry.save()
            messages.success(request, 'Your inquiry has been submitted.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = InquiryForm()
    return render(request, '/', {'form': form})

@login_required
def inquiry(request):
    # Fetch inquiries related to the logged-in user
    inquiries = Inquiry.objects.filter(user=request.user)
    return render(request, 'inquiry.html', {'inquiries': inquiries})

@login_required
def feedback(request ):
    destinations = Destination.objects.all()
    return render(request, 'feedback.html' , {'destinations': destinations})

@login_required
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, 'Your feedback has been submitted.')
            return redirect('/')
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})