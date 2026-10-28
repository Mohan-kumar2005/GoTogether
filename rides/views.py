from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Ride
from .forms import RideCreateForm
from datetime import date

@login_required
def create_ride_view(request):
    profile = request.user.profile
    # Alert if profile lacks driving license or vehicle
    if not profile.has_driving_license and not profile.driving_license_no:
        messages.warning(request, "⚠️ Notice: For community safety and trust, please make sure your Driving License is updated on your profile.")

    if request.method == 'POST':
        form = RideCreateForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.driver = request.user
            ride.available_seats = ride.total_seats
            
            # Enforce 2-wheeler helmet safety rule
            if ride.vehicle_type == '2_WHEELER':
                ride.is_helmet_mandatory = True
                if ride.total_seats > 1:
                    ride.total_seats = 1
                    ride.available_seats = 1
                    
            ride.save()
            messages.success(request, f"🎉 Ride from {ride.source_city} to {ride.destination_city} posted successfully!")
            return redirect('ride_details', ride_id=ride.id)
    else:
        # Pre-populate defaults from user profile
        initial_data = {
            'departure_date': date.today(),
            'vehicle_type': profile.vehicle_type if profile.vehicle_type in ['2_WHEELER', '4_WHEELER'] else '4_WHEELER',
            'vehicle_model': profile.vehicle_name_model or '',
            'vehicle_number': profile.vehicle_number or '',
            'total_seats': 1 if profile.vehicle_type == '2_WHEELER' else 3,
            'is_helmet_mandatory': True,
        }
        form = RideCreateForm(initial=initial_data)

    return render(request, 'create_ride.html', {'form': form})


def find_ride_view(request):
    # Query parameters
    source = request.GET.get('source', '').strip()
    destination = request.GET.get('destination', '').strip()
    travel_date = request.GET.get('date', '').strip()
    vehicle_type = request.GET.get('vehicle_type', '').strip()
    festival = request.GET.get('festival', '').strip()
    swap_driving = request.GET.get('swap_driving', '').strip()

    rides = Ride.objects.filter(status='ACTIVE', available_seats__gt=0).select_related('driver', 'driver__profile')

    if source:
        rides = rides.filter(source_city__icontains=source)
    if destination:
        rides = rides.filter(destination_city__icontains=destination)
    if travel_date:
        rides = rides.filter(departure_date=travel_date)
    if vehicle_type and vehicle_type in ['2_WHEELER', '4_WHEELER']:
        rides = rides.filter(vehicle_type=vehicle_type)
    if festival and festival != 'ALL':
        rides = rides.filter(festival=festival)
    if swap_driving == 'yes':
        rides = rides.filter(open_to_swap_driving=True)

    festivals = Ride.FESTIVAL_CHOICES

    return render(request, 'find_ride.html', {
        'rides': rides,
        'source': source,
        'destination': destination,
        'travel_date': travel_date,
        'vehicle_type': vehicle_type,
        'festival': festival,
        'swap_driving': swap_driving,
        'festivals': festivals,
        'total_found': rides.count(),
    })


def ride_details_view(request, ride_id):
    ride = get_object_or_404(Ride.objects.select_related('driver', 'driver__profile'), id=ride_id)
    
    # Calculate comparative savings compared to festive Omni Bus ticket
    # Typical bus ticket surge in Tamil Nadu during festivals: ₹800 to ₹2200
    base_bus_fare = max(600, int(ride.estimated_distance_km * 3.5)) if ride.estimated_distance_km else 950
    savings = max(0, int(base_bus_fare - float(ride.cost_per_seat)))

    user_has_requested = False
    existing_request = None
    if request.user.is_authenticated:
        existing_request = ride.requests.filter(passenger=request.user).first()
        if existing_request:
            user_has_requested = True

    accepted_passengers = ride.requests.filter(status='ACCEPTED').select_related('passenger', 'passenger__profile')

    return render(request, 'ride_details.html', {
        'ride': ride,
        'base_bus_fare': base_bus_fare,
        'savings': savings,
        'user_has_requested': user_has_requested,
        'existing_request': existing_request,
        'accepted_passengers': accepted_passengers,
        'is_driver': (request.user == ride.driver if request.user.is_authenticated else False),
    })


@login_required
def my_rides_view(request):
    rides = Ride.objects.filter(driver=request.user).order_by('-created_at')
    return render(request, 'my_rides.html', {'rides': rides})


@login_required
def edit_ride_view(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id, driver=request.user)

    if request.method == 'POST':
        if 'cancel_ride' in request.POST:
            ride.status = 'CANCELLED'
            ride.save()
            messages.info(request, "Ride has been cancelled.")
            return redirect('my_rides')

        form = RideCreateForm(request.POST, instance=ride)
        if form.is_valid():
            r = form.save(commit=False)
            r.update_available_seats()
            messages.success(request, "Ride details updated successfully!")
            return redirect('ride_details', ride_id=ride.id)
    else:
        form = RideCreateForm(instance=ride)

    return render(request, 'edit_ride.html', {'form': form, 'ride': ride})
