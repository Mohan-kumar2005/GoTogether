from django.urls import path
from . import views

urlpatterns = [
    path('request/<int:ride_id>/', views.request_ride_view, name='request_ride'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('detail/<int:booking_id>/', views.booking_detail_view, name='booking_detail'),
    path('ride-requests/', views.ride_requests_view, name='ride_requests'),
    path('ride-requests/<int:ride_id>/', views.ride_requests_view, name='ride_specific_requests'),
    path('respond/<int:booking_id>/<str:action>/', views.respond_request_view, name='respond_request'),
    path('cancel/<int:booking_id>/', views.cancel_booking_view, name='cancel_booking'),
    path('review/<int:booking_id>/', views.add_review_view, name='add_review'),
]
