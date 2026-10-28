from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class SignUpForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'e.g. yourname@gmail.com'})
    )
    phone_number = forms.CharField(
        max_length=15, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter 10-digit Mobile Number'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create a Secure Password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        }


    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone:
            phone = phone.strip().replace(' ', '').replace('-', '')
            if UserProfile.objects.filter(phone_number=phone).exists():
                raise forms.ValidationError("This phone number is already registered.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("confirm_password")
        if p1 and p2 and p1 != p2:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = [
            'bio', 'gender', 'avatar',
            'has_driving_license', 'driving_license_no', 'driving_license_image', 'can_swap_drive',
            'owns_vehicle', 'vehicle_type', 'vehicle_name_model', 'vehicle_number',
            'emergency_contact_name', 'emergency_contact_phone'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell co-travelers about yourself...'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'has_driving_license': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_has_license'}),
            'driving_license_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. TN4720180001234'}),
            'driving_license_image': forms.FileInput(attrs={'class': 'form-control'}),
            'can_swap_drive': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'owns_vehicle': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_owns_vehicle'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-select'}),
            'vehicle_name_model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. RE Classic 350 / Hyundai i20'}),
            'vehicle_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. TN 47 AB 1234'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Guardian / Friend Name'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency Mobile Number'}),
        }
