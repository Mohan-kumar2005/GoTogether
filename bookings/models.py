from django.db import models
from django.contrib.auth.models import User
from rides.models import Ride

class RideRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Driver Approval ⏳'),
        ('ACCEPTED', 'Accepted & Confirmed ✅'),
        ('REJECTED', 'Declined ❌'),
        ('CANCELLED', 'Cancelled by Passenger 🚫'),
    ]

    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='requests')
    passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ride_bookings')
    seats_booked = models.PositiveSmallIntegerField(default=1)
    
    # Crucial User Requirement: Stranger driving knowledge & swap driving capability
    knows_driving = models.BooleanField(
        default=False, 
        help_text="Does the stranger know driving and hold a valid license?"
    )
    willing_to_swap_driving = models.BooleanField(
        default=False, 
        help_text="Stranger is willing to take turns driving to help the driver rest on long festival journeys"
    )
    license_number = models.CharField(max_length=30, blank=True, null=True, help_text="Driving License number if willing to swap")
    license_document = models.ImageField(upload_to='passenger_licenses/', blank=True, null=True)
    
    # Crucial User Requirement: 2-Wheeler Helmet mandatory confirmation
    confirmed_helmet = models.BooleanField(
        default=False, 
        help_text="Passenger acknowledges and confirms wearing a certified helmet for 2-wheeler ride"
    )
    
    pickup_note = models.CharField(max_length=200, blank=True, null=True, help_text="Preferred landmark or pickup note")
    passenger_message = models.TextField(blank=True, null=True, help_text="Message for driver regarding bags, timing, etc.")
    
    total_fare = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Request by {self.passenger.username} for {self.ride} ({self.status})"

    def save(self, *args, **kwargs):
        if not self.total_fare and self.ride:
            self.total_fare = self.seats_booked * self.ride.cost_per_seat
        super().save(*args, **kwargs)


class RideReview(models.Model):
    booking = models.ForeignKey(RideRequest, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    rating = models.PositiveSmallIntegerField(default=5) # 1 to 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review from {self.reviewer.username} to {self.reviewee.username} ({self.rating}★)"
