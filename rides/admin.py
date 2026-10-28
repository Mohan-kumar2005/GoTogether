from django.contrib import admin
from .models import Ride

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ('source_city', 'destination_city', 'departure_date', 'departure_time', 'vehicle_type', 'available_seats', 'cost_per_seat', 'festival', 'status')
    list_filter = ('vehicle_type', 'festival', 'status', 'open_to_swap_driving', 'is_helmet_mandatory')
    search_fields = ('source_city', 'destination_city', 'driver__username', 'vehicle_model')
