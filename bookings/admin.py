from django.contrib import admin
from .models import RideRequest, RideReview

@admin.register(RideRequest)
class RideRequestAdmin(admin.ModelAdmin):
    list_display = ('ride', 'passenger', 'seats_booked', 'knows_driving', 'willing_to_swap_driving', 'confirmed_helmet', 'status', 'total_fare', 'created_at')
    list_filter = ('status', 'knows_driving', 'willing_to_swap_driving', 'confirmed_helmet')
    search_fields = ('passenger__username', 'ride__source_city', 'ride__destination_city')

@admin.register(RideReview)
class RideReviewAdmin(admin.ModelAdmin):
    list_display = ('booking', 'reviewer', 'reviewee', 'rating', 'created_at')
