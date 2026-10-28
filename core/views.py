from django.shortcuts import render, redirect
from django.contrib import messages
from rides.models import Ride
from .models import ContactMessage
from accounts.models import UserProfile

def home_view(request):
    featured_rides = Ride.objects.filter(status='ACTIVE', available_seats__gt=0).select_related('driver', 'driver__profile').order_by('departure_date', 'departure_time')[:6]
    two_wheeler_rides = Ride.objects.filter(status='ACTIVE', vehicle_type='2_WHEELER', available_seats__gt=0).count()
    four_wheeler_rides = Ride.objects.filter(status='ACTIVE', vehicle_type='4_WHEELER', available_seats__gt=0).count()
    total_active_rides = Ride.objects.filter(status='ACTIVE').count()
    verified_users_count = UserProfile.objects.filter(is_phone_verified=True).count()

    return render(request, 'home.html', {
        'featured_rides': featured_rides,
        'two_wheeler_rides_count': two_wheeler_rides,
        'four_wheeler_rides_count': four_wheeler_rides,
        'total_active_rides': total_active_rides,
        'verified_users_count': verified_users_count,
        'festivals': Ride.FESTIVAL_CHOICES,
    })


def about_view(request):
    return render(request, 'about.html')


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and message:
            ContactMessage.objects.create(
                name=name, email=email, phone=phone,
                subject=subject, message=message
            )
            messages.success(request, "🙏 Thank you for reaching out! Our GoTogether support team will get back to you shortly.")
            return redirect('contact')
        else:
            messages.error(request, "Please fill in all required fields.")

    return render(request, 'contact.html')
