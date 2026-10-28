from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Ride(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('2_WHEELER', '2-Wheeler (Bike / Scooter)'),
        ('4_WHEELER', '4-Wheeler (Car)'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active / Accepting Passengers'),
        ('FULL', 'Fully Booked'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    FESTIVAL_CHOICES = [
        ('NONE', 'Regular Travel / Weekend'),
        ('DIWALI', 'Diwali Festival Rush 🪔'),
        ('PONGAL', 'Pongal Festival Rush 🌾'),
        ('AAYUTHA_POOJA', 'Aayutha Pooja / Dussehra ⚔️'),
        ('CHRISTMAS_NY', 'Christmas & New Year 🎄'),
        ('SUMMER_VACATION', 'Summer Holiday Travel ☀️'),
        ('OTHER_FESTIVAL', 'Other Special Festival 🎊'),
    ]

    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides_offered')
    source_city = models.CharField(max_length=100, help_text="e.g. Karur, Coimbatore, Chennai, Trichy")
    destination_city = models.CharField(max_length=100, help_text="e.g. Chennai, Karur, Madurai, Bangalore")
    pickup_point = models.CharField(max_length=200, help_text="Specific pickup spot, e.g., Karur Bus Stand or Gandhipuram")
    drop_point = models.CharField(max_length=200, help_text="Specific drop location, e.g., Koyambedu, Tambaram, or Guindy")
    
    departure_date = models.DateField()
    departure_time = models.TimeField()
    
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES, default='4_WHEELER')
    vehicle_model = models.CharField(max_length=100, help_text="e.g. Royal Enfield Hunter 350, Honda Activa, Swift, i20")
    vehicle_number = models.CharField(max_length=30, help_text="e.g. TN 47 AB 1234")
    
    total_seats = models.PositiveSmallIntegerField(default=3, help_text="Max 1 for 2-wheeler, up to 6 for 4-wheeler")
    available_seats = models.PositiveSmallIntegerField(default=3)
    
    estimated_distance_km = models.PositiveIntegerField(default=100, help_text="Approximate trip distance in km")
    total_estimated_fuel_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, help_text="Estimated petrol/diesel cost for entire trip (₹)")
    cost_per_seat = models.DecimalField(max_digits=7, decimal_places=2, help_text="Fair fuel share cost per seat (₹)")
    
    festival = models.CharField(max_length=30, choices=FESTIVAL_CHOICES, default='NONE')
    
    # 2-Wheeler Helmet Safety Policy
    is_helmet_mandatory = models.BooleanField(default=True, help_text="Strictly mandatory for 2-wheeler rides")
    has_spare_helmet = models.BooleanField(default=False, help_text="Driver provides a spare helmet for pillion passenger")
    
    # Swap Driving Capability for Long Road Trips
    open_to_swap_driving = models.BooleanField(
        default=False, 
        help_text="Driver invites/welcomes a stranger with a valid license to swap driving to take rest"
    )
    
    luggage_space = models.CharField(
        max_length=50, 
        choices=[
            ('SMALL_BAG', 'Small Backpack Only (Ideal for 2-wheeler)'),
            ('MEDIUM', 'Medium Bag / Trolley'),
            ('LARGE', 'Heavy Luggage / Multiple Bags')
        ], 
        default='MEDIUM'
    )
    
    additional_notes = models.TextField(blank=True, null=True, help_text="Preferences: AC, No smoking, music, intermediate stops, etc.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['departure_date', 'departure_time']

    def __str__(self):
        return f"{self.source_city} ➔ {self.destination_city} ({self.departure_date}) by {self.driver.username}"

    def is_two_wheeler(self):
        return self.vehicle_type == '2_WHEELER'

    def update_available_seats(self):
        booked = sum(self.requests.filter(status='ACCEPTED').values_list('seats_booked', flat=True))
        self.available_seats = max(0, self.total_seats - booked)
        if self.available_seats == 0 and self.status == 'ACTIVE':
            self.status = 'FULL'
        elif self.available_seats > 0 and self.status == 'FULL':
            self.status = 'ACTIVE'
        self.save()
