import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from flights.models import Flight
from .models import Booking

logger = logging.getLogger(__name__)


@login_required
def book_flight(request, flight_id):
    """
    Create a new flight booking for the authenticated user.
    
    Process:
    1. Check flight availability
    2. Create booking record
    3. Decrement available seats
    4. Log the booking action
    """
    flight = get_object_or_404(Flight, pk=flight_id)

    if flight.seats_available <= 0:
        logger.warning(
            f'User {request.user.username} attempted to book flight {flight.id} with no seats available'
        )
        return render(request, "booking/no_seat.html", {"flight": flight})

    booking = Booking.objects.create(
        user=request.user,
        flight=flight,
        price_paid=flight.price
    )

    flight.seats_available -= 1
    flight.save()

    logger.info(
        f'User {request.user.username} booked flight {flight.id} ({flight.origin} -> {flight.destination}). '
        f'Booking ID: {booking.id}, Price: {flight.price}'
    )

    return redirect("booking:my_bookings")


@login_required
def my_bookings(request):
    """
    Display all bookings for the authenticated user.
    
    Shows active and canceled bookings with booking details.
    """
    bookings = Booking.objects.filter(user=request.user)
    logger.info(f'User {request.user.username} viewed their bookings ({bookings.count()} total)')
    return render(request, "booking/my_bookings.html", {"bookings": bookings})


@login_required
def cancel_booking(request, booking_id):
    """
    Cancel an existing booking and process refund.
    
    Process:
    1. Verify booking ownership
    2. Calculate penalty and refund
    3. Update booking status
    4. Restore available seats
    5. Log cancellation
    """
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)

    if booking.status == "canceled":
        logger.info(f'User {request.user.username} attempted to cancel already-canceled booking {booking_id}')
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

    logger.info(
        f'User {request.user.username} canceled booking {booking_id}. '
        f'Original Price: {booking.price_paid}, Penalty: {penalty_amount}, Refund: {booking.final_refund}'
    )

    return redirect("booking:my_bookings")