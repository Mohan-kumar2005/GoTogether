from django.urls import path
from . import views

urlpatterns = [
    path('find/', views.find_ride_view, name='find_ride'),
    path('create/', views.create_ride_view, name='create_ride'),
    path('my-rides/', views.my_rides_view, name='my_rides'),
    path('details/<int:ride_id>/', views.ride_details_view, name='ride_details'),
    path('edit/<int:ride_id>/', views.edit_ride_view, name='edit_ride'),
]
