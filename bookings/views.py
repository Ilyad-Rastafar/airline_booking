from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from flights.models import Flight
from .models import Booking
from django.utils import timezone

@login_required
def book_flight(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)

    if flight.seats_available <= 0:
        return render(request, "booking/no_seat.html", {"flight": flight})

    booking = Booking.objects.create(
        user=request.user,
        flight=flight,
        price_paid=flight.price
    )

    flight.seats_available -= 1
    flight.save()

    return redirect("booking:my_bookings")


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "booking/my_bookings.html", {"bookings": bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)

    if booking.status == "canceled":
        return redirect("booking:my_bookings")

    penalty_percent = booking.flight.cancel_penalty_percent
    penalty_amount = booking.price_paid * penalty_percent // 100

    booking.status = "canceled"
    booking.penalty_amount = penalty_amount
    booking.final_refund = booking.price_paid - penalty_amount
    booking.canceled_at = timezone.now()
    booking.save()

    flight = booking.flight
    flight.seats_available += 1
    flight.save()

    return redirect("booking:my_bookings")