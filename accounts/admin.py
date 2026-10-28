from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'is_phone_verified', 'has_driving_license', 'is_license_verified', 'vehicle_type', 'can_swap_drive')
    list_filter = ('is_phone_verified', 'is_license_verified', 'vehicle_type', 'can_swap_drive')
    search_fields = ('user__username', 'phone_number', 'driving_license_no')
