from django import forms
from .models import RideRequest, RideReview

class RideRequestForm(forms.ModelForm):
    class Meta:
        model = RideRequest
        fields = [
            'seats_booked', 'knows_driving', 'willing_to_swap_driving',
            'license_number', 'license_document', 'confirmed_helmet',
            'pickup_note', 'passenger_message'
        ]
        widgets = {
            'seats_booked': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'id': 'id_seats_booked'}),
            'knows_driving': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_knows_driving'}),
            'willing_to_swap_driving': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_willing_to_swap'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. DL-1420110012345'}),
            'license_document': forms.FileInput(attrs={'class': 'form-control'}),
            'confirmed_helmet': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_confirmed_helmet'}),
            'pickup_note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Specific pickup spot / landmark'}),
            'passenger_message': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Any note for the driver (luggage size, phone number, etc.)'}),
        }

    def __init__(self, *args, **kwargs):
        self.ride = kwargs.pop('ride', None)
        super().__init__(*args, **kwargs)
        if self.ride:
            max_available = self.ride.available_seats
            self.fields['seats_booked'].widget.attrs['max'] = max_available
            if self.ride.vehicle_type == '2_WHEELER':
                self.fields['seats_booked'].initial = 1
                self.fields['seats_booked'].widget.attrs['max'] = 1
                self.fields['seats_booked'].widget.attrs['readonly'] = True


class RideReviewForm(forms.ModelForm):
    class Meta:
        model = RideReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(5, '⭐⭐⭐⭐⭐ Excellent (5/5)'), (4, '⭐⭐⭐⭐ Good (4/5)'), (3, '⭐⭐⭐ Average (3/5)'), (2, '⭐⭐ Below Average (2/5)'), (1, '⭐ Poor (1/5)')], attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Share how the ride went (punctuality, driving skill, friendliness)...'}),
        }
