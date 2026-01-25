from django.urls import path
from .views import (
    services,
    dog_grooming,
    cat_grooming,
    pet_boarding,
    create_booking,
    my_bookings,
    cancel_booking,


)

urlpatterns = [
    path('', services, name='services'),
    path('dog_grooming/', dog_grooming, name='dog_grooming'),
    path('cat_grooming/', cat_grooming, name='cat_grooming'),
    path('pet_boarding/', pet_boarding, name='pet_boarding'),

    # ✅ AJAX booking endpoint
    path('create-booking/', create_booking, name='create_booking'),
    path('my-bookings/', my_bookings, name='my_bookings'),
    path('cancel-booking/<str:booking_id>/', cancel_booking, name='cancel_booking'),
]


