from django import forms
from .models import Ride
from datetime import date

class RideCreateForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = [
            'source_city', 'destination_city', 'pickup_point', 'drop_point',
            'departure_date', 'departure_time', 'vehicle_type', 'vehicle_model',
            'vehicle_number', 'total_seats', 'estimated_distance_km',
            'total_estimated_fuel_cost', 'cost_per_seat', 'festival',
            'is_helmet_mandatory', 'has_spare_helmet', 'open_to_swap_driving',
            'luggage_space', 'additional_notes'
        ]
        widgets = {
            'source_city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Karur'}),
            'destination_city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Chennai'}),
            'pickup_point': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Karur Bus Stand, Light House'}),
            'drop_point': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Koyambedu Bus Terminus / Tambaram'}),
            'departure_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'departure_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-select', 'id': 'id_vehicle_type'}),
            'vehicle_model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Royal Enfield Hunter 350 / Swift VXi'}),
            'vehicle_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. TN 47 AB 1234'}),
            'total_seats': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 6, 'id': 'id_total_seats'}),
            'estimated_distance_km': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_distance_km'}),
            'total_estimated_fuel_cost': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_fuel_cost'}),
            'cost_per_seat': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_cost_per_seat'}),
            'festival': forms.Select(attrs={'class': 'form-select'}),
            'is_helmet_mandatory': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_helmet_mandatory'}),
            'has_spare_helmet': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'open_to_swap_driving': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'luggage_space': forms.Select(attrs={'class': 'form-select'}),
            'additional_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'e.g. AC available, non-smoking, polite passengers welcome, sharing toll costs equally.'}),
        }

    def clean_departure_date(self):
        dep_date = self.cleaned_data.get('departure_date')
        if dep_date and dep_date < date.today():
            raise forms.ValidationError("Departure date cannot be in the past.")
        return dep_date

    def clean(self):
        cleaned_data = super().clean()
        v_type = cleaned_data.get('vehicle_type')
        seats = cleaned_data.get('total_seats')

        # Safety & physical validation: 2-wheeler can only carry 1 co-passenger
        if v_type == '2_WHEELER':
            if seats and seats > 1:
                self.add_error('total_seats', "A 2-wheeler can only carry 1 co-passenger (pillion rider).")
            # Helmets are mandatory for 2-wheelers
            cleaned_data['is_helmet_mandatory'] = True

        return cleaned_data
