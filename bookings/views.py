from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import RideRequest, RideReview
from .forms import RideRequestForm, RideReviewForm
from rides.models import Ride

@login_required
def request_ride_view(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)

    if ride.driver == request.user:
        messages.warning(request, "You cannot book your own ride!")
        return redirect('ride_details', ride_id=ride.id)

    if ride.available_seats <= 0:
        messages.error(request, "Sorry, this ride has no remaining seats.")
        return redirect('ride_details', ride_id=ride.id)

    # Check if user already requested
    existing = RideRequest.objects.filter(ride=ride, passenger=request.user).first()
    if existing:
        messages.info(request, f"You have already requested this ride (Status: {existing.get_status_display()}).")
        return redirect('booking_detail', booking_id=existing.id)

    profile = request.user.profile

    if request.method == 'POST':
        form = RideRequestForm(request.POST, request.FILES, ride=ride)
        if form.is_valid():
            req = form.save(commit=False)
            req.ride = ride
            req.passenger = request.user

            # Two-wheeler helmet validation
            if ride.vehicle_type == '2_WHEELER':
                if not req.confirmed_helmet:
                    messages.error(request, "⚠️ Mandatory Safety Rule: You must confirm that you will wear a certified helmet for a 2-wheeler trip!")
                    return render(request, 'request_ride.html', {'form': form, 'ride': ride, 'profile': profile})
                req.seats_booked = 1

            if req.seats_booked > ride.available_seats:
                messages.error(request, f"Only {ride.available_seats} seat(s) available.")
                return render(request, 'request_ride.html', {'form': form, 'ride': ride, 'profile': profile})

            # Calculate total fare
            req.total_fare = req.seats_booked * ride.cost_per_seat

            # If user uploaded license here, update profile too
            if req.license_document or req.license_number:
                profile.has_driving_license = True
                if req.license_number:
                    profile.driving_license_no = req.license_number
                if req.license_document:
                    profile.driving_license_image = req.license_document
                if req.willing_to_swap_driving:
                    profile.can_swap_drive = True
                profile.is_license_verified = True
                profile.save()

            req.save()
            messages.success(request, f"🎉 Request sent to {ride.driver.username}! You will be notified once they accept.")
            return redirect('booking_detail', booking_id=req.id)
    else:
        # Prepopulate with profile data if available
        initial_data = {
            'seats_booked': 1,
            'knows_driving': profile.has_driving_license or profile.can_swap_drive,
            'willing_to_swap_driving': profile.can_swap_drive,
            'license_number': profile.driving_license_no or '',
            'confirmed_helmet': True if ride.vehicle_type == '2_WHEELER' else False,
        }
        form = RideRequestForm(initial=initial_data, ride=ride)

    return render(request, 'request_ride.html', {
        'form': form,
        'ride': ride,
        'profile': profile,
    })


@login_required
def my_bookings_view(request):
    bookings = RideRequest.objects.filter(passenger=request.user).select_related('ride', 'ride__driver', 'ride__driver__profile')
    return render(request, 'my_bookings.html', {'bookings': bookings})


@login_required
def booking_detail_view(request, booking_id):
    booking = get_object_or_404(
        RideRequest.objects.select_related('ride', 'ride__driver', 'ride__driver__profile', 'passenger', 'passenger__profile'),
        id=booking_id
    )

    # Permission check: must be either passenger or ride driver
    if request.user != booking.passenger and request.user != booking.ride.driver:
        messages.error(request, "You are not authorized to view this booking.")
        return redirect('home')

    review_form = RideReviewForm()
    user_review = RideReview.objects.filter(booking=booking, reviewer=request.user).first()

    return render(request, 'booking_detail.html', {
        'booking': booking,
        'review_form': review_form,
        'user_review': user_review,
        'is_passenger': (request.user == booking.passenger),
        'is_driver': (request.user == booking.ride.driver),
    })


@login_required
def ride_requests_view(request, ride_id=None):
    if ride_id:
        ride = get_object_or_404(Ride, id=ride_id, driver=request.user)
        requests = RideRequest.objects.filter(ride=ride).select_related('passenger', 'passenger__profile', 'ride')
    else:
        ride = None
        requests = RideRequest.objects.filter(ride__driver=request.user).select_related('passenger', 'passenger__profile', 'ride').order_by('-created_at')

    return render(request, 'ride_requests.html', {
        'requests': requests,
        'ride': ride,
    })


@login_required
def respond_request_view(request, booking_id, action):
    booking = get_object_or_404(RideRequest, id=booking_id, ride__driver=request.user)
    ride = booking.ride

    if action == 'accept':
        if ride.available_seats >= booking.seats_booked:
            booking.status = 'ACCEPTED'
            booking.save()
            ride.update_available_seats()
            messages.success(request, f"✅ Accepted booking for {booking.passenger.username}! You can now coordinate travel.")
        else:
            messages.error(request, "Cannot accept: Not enough seats remaining.")
    elif action == 'reject':
        booking.status = 'REJECTED'
        booking.save()
        ride.update_available_seats()
        messages.info(request, f"Declined request from {booking.passenger.username}.")

    return redirect('ride_requests')


@login_required
def cancel_booking_view(request, booking_id):
    booking = get_object_or_404(RideRequest, id=booking_id, passenger=request.user)
    ride = booking.ride

    booking.status = 'CANCELLED'
    booking.save()
    ride.update_available_seats()
    messages.info(request, "Your booking request has been cancelled.")
    return redirect('my_bookings')


@login_required
def add_review_view(request, booking_id):
    booking = get_object_or_404(RideRequest, id=booking_id)

    if request.user != booking.passenger and request.user != booking.ride.driver:
        messages.error(request, "Unauthorized")
        return redirect('home')

    # Determine who is being reviewed
    if request.user == booking.passenger:
        target_user = booking.ride.driver
    else:
        target_user = booking.passenger

    if request.method == 'POST':
        form = RideReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.reviewer = request.user
            review.reviewee = target_user
            review.save()
            messages.success(request, f"🌟 Thank you for reviewing {target_user.username}!")
            return redirect('booking_detail', booking_id=booking.id)

    return redirect('booking_detail', booking_id=booking.id)
