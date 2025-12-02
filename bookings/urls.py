from django.urls import path
from .views import book_flight, my_bookings, cancel_booking

app_name = "booking"

urlpatterns = [
    path("book/<int:flight_id>/", book_flight, name="book_flight"),
    path("my/", my_bookings, name="my_bookings"),
    path("cancel/<int:booking_id>/", cancel_booking, name="cancel_booking"),
]