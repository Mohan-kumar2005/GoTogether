from bookings.models import RideRequest

def global_context(request):
    pending_count = 0
    if request.user.is_authenticated:
        # Rides created by this user that have pending booking requests
        pending_count = RideRequest.objects.filter(
            ride__driver=request.user,
            status='PENDING'
        ).count()
        
    return {
        'SITE_NAME': 'GoTogether',
        'SITE_TAGLINE': 'Share Rides • Share Costs • Reach Home',
        'pending_requests_count': pending_count,
        'QUICK_ROUTES': [
            {'from': 'Karur', 'to': 'Chennai', 'type': '4_WHEELER'},
            {'from': 'Coimbatore', 'to': 'Karur', 'type': '2_WHEELER'},
            {'from': 'Chennai', 'to': 'Trichy', 'type': '4_WHEELER'},
            {'from': 'Bangalore', 'to': 'Salem', 'type': '4_WHEELER'},
            {'from': 'Madurai', 'to': 'Chennai', 'type': '4_WHEELER'},
            {'from': 'Erode', 'to': 'Coimbatore', 'type': '2_WHEELER'},
        ]
    }
