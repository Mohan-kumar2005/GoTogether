from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import random

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    VEHICLE_CHOICES = [
        ('NONE', 'No Vehicle (Passenger)'),
        ('2_WHEELER', '2-Wheeler (Bike / Scooter)'),
        ('4_WHEELER', '4-Wheeler (Car)'),
        ('BOTH', 'Both 2-Wheeler & 4-Wheeler'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    is_phone_verified = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    
    bio = models.TextField(blank=True, null=True, help_text="Short bio about yourself, travel habits, hometown, etc.")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    # Driving License details for safety & swap driving
    has_driving_license = models.BooleanField(default=False)
    driving_license_no = models.CharField(max_length=30, blank=True, null=True)
    driving_license_image = models.ImageField(upload_to='licenses/', null=True, blank=True)
    is_license_verified = models.BooleanField(default=False)
    can_swap_drive = models.BooleanField(default=False, help_text="Willing and eligible to share/swap driving on long trips")
    
    # Vehicle details
    owns_vehicle = models.BooleanField(default=False)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_CHOICES, default='NONE')
    vehicle_name_model = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. Royal Enfield Hunter 350 or Hyundai i20")
    vehicle_number = models.CharField(max_length=30, blank=True, null=True, help_text="e.g. TN 47 AB 1234")
    
    # Emergency contact
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def generate_otp(self):
        """Generates a 6-digit verification OTP."""
        otp = str(random.randint(100000, 999999))
        self.otp_code = otp
        self.otp_created_at = timezone.now()
        self.save()
        return otp

    def verify_otp(self, code):
        """Validates the OTP code within 15 minutes."""
        if not self.otp_code or not self.otp_created_at:
            return False, "No OTP was generated."
        
        # Check expiration (15 minutes)
        diff = (timezone.now() - self.otp_created_at).total_seconds()
        if diff > 900:
            return False, "OTP has expired. Please request a new one."
        
        if str(self.otp_code).strip() == str(code).strip():
            self.is_phone_verified = True
            self.otp_code = None
            self.save()
            return True, "Phone number successfully verified!"
        return False, "Invalid OTP code entered."

    @property
    def dl_status_badge(self):
        if self.is_license_verified:
            return "badge-verified"
        elif self.driving_license_image or self.driving_license_no:
            return "badge-pending"
        return "badge-unverified"

@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
        else:
            UserProfile.objects.create(user=instance)
