import logging
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Flight
from .forms import SearchForm

logger = logging.getLogger(__name__)


@login_required
def flight_list(request):
    """
    Display list of available flights with optional search filtering.
    
    Search criteria:
    - origin: Departure city
    - destination: Arrival city
    - date: Flight date
    """
    form = SearchForm(request.GET or None)
    flights = Flight.objects.all()

    search_params = {}
    if form.is_valid():
        origin = form.cleaned_data.get("origin")
        destination = form.cleaned_data.get("destination")
        date = form.cleaned_data.get("date")

        if origin:
            flights = flights.filter(route__origin__icontains=origin)
            search_params['origin'] = origin

        if destination:
            flights = flights.filter(route__destination__icontains=destination)
            search_params['destination'] = destination

        if date:
            flights = flights.filter(departure_time__date=date)
            search_params['date'] = date

        logger.info(
            f'User {request.user.username} searched for flights with params: {search_params}'
        )

    return render(request, "flights/list.html", {"form": form, "flights": flights})


@login_required
def flight_detail(request, pk):
    """
    Display detailed information about a specific flight.
    """
    flight = get_object_or_404(Flight, pk=pk)
    logger.info(f'User {request.user.username} viewed flight detail: {flight}')
    return render(request, "flights/detail.html", {"flight": flight})
