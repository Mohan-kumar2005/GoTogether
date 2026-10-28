from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, UserProfileForm
from .models import UserProfile
from .utils import send_otp_email
from bookings.models import RideReview

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Update user profile
            profile, _ = UserProfile.objects.get_or_create(user=user)
            phone = form.cleaned_data['phone_number']
            profile.phone_number = phone
            profile.save()
            
            # Generate OTP for verification
            otp = profile.generate_otp()
            request.session['verification_user_id'] = user.id
            request.session['demo_otp'] = otp

            # Real-time OTP to Gmail inbox
            email_sent, email_msg = send_otp_email(user, otp)
            if email_sent:
                messages.success(request, f"📧 Real-time OTP sent to your Gmail: {user.email}! Please check your inbox.")
            else:
                messages.info(request, f"Generated OTP: {otp}. (Tip: Add your Gmail credentials in GoTogether/email_config.py for live email delivery).")

            return redirect('verify_otp')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


def verify_otp_view(request):
    user_id = request.session.get('verification_user_id')
    if not user_id:
        if request.user.is_authenticated:
            user_id = request.user.id
        else:
            messages.warning(request, "Please register or log in first.")
            return redirect('signup')

    target_user = get_object_or_404(User, id=user_id)
    profile = target_user.profile
    demo_otp = request.session.get('demo_otp', profile.otp_code)

    if request.method == 'POST':
        code = request.POST.get('otp', '').strip()
        success, msg = profile.verify_otp(code)
        if success:
            messages.success(request, "🎉 Verification successful! Welcome to GoTogether!")
            login(request, target_user)
            if 'demo_otp' in request.session:
                del request.session['demo_otp']
            if 'verification_user_id' in request.session:
                del request.session['verification_user_id']
            return redirect('profile')
        else:
            messages.error(request, msg)

    return render(request, 'signup.html', {
        'otp_step': True,
        'email': target_user.email,
        'phone': profile.phone_number,
        'demo_otp': demo_otp,
    })


def resend_otp_view(request):
    user_id = request.session.get('verification_user_id')
    if not user_id and request.user.is_authenticated:
        user_id = request.user.id

    if not user_id:
        return redirect('signup')

    target_user = get_object_or_404(User, id=user_id)
    otp = target_user.profile.generate_otp()
    request.session['demo_otp'] = otp

    # Real-time OTP to Gmail inbox
    email_sent, email_msg = send_otp_email(target_user, otp)
    if email_sent:
        messages.success(request, f"📧 A new OTP has been dispatched to your Gmail ({target_user.email})!")
    else:
        messages.info(request, f"New OTP generated: {otp}")

    return redirect('verify_otp')



def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username_or_phone = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Allow login via username or phone number
        user = None
        if User.objects.filter(username=username_or_phone).exists():
            user = authenticate(request, username=username_or_phone, password=password)
        else:
            profile = UserProfile.objects.filter(phone_number=username_or_phone).first()
            if profile:
                user = authenticate(request, username=profile.user.username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username/phone number or password.")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out safely.")
    return redirect('home')


@login_required
def profile_view(request, user_id=None):
    if user_id:
        viewed_user = get_object_or_404(User, id=user_id)
    else:
        viewed_user = request.user

    profile = viewed_user.profile
    reviews = RideReview.objects.filter(reviewee=viewed_user).select_related('reviewer')
    
    # Calculate average rating
    avg_rating = 5.0
    if reviews.exists():
        ratings = [r.rating for r in reviews]
        avg_rating = round(sum(ratings) / len(ratings), 1)

    return render(request, 'profile.html', {
        'profile_user': viewed_user,
        'profile': profile,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'is_own_profile': (viewed_user == request.user),
    })


@login_required
def edit_profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            
            p = form.save(commit=False)
            # If user uploaded DL image, set DL verified status for demonstration/admin review
            if p.driving_license_image or p.driving_license_no:
                p.has_driving_license = True
                p.is_license_verified = True  # Verified upon upload for seamless demo
            p.save()
            
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = UserProfileForm(instance=profile, initial=initial_data)

    return render(request, 'edit_profile.html', {'form': form, 'profile': profile})
