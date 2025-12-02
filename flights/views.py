from django.shortcuts import render, get_object_or_404, redirect
from .models import Flight
from .forms import SearchForm

def flight_list(request):
    form = SearchForm(request.GET or None)
    flights = Flight.objects.all()

    if form.is_valid():
        if form.cleaned_data["origin"]:
            flights = flights.filter(route__origin__icontains=form.cleaned_data["origin"])
        if form.cleaned_data["destination"]:
            flights = flights.filter(route__destination__icontains=form.cleaned_data["destination"])
        if form.cleaned_data["date"]:
            flights = flights.filter(date=form.cleaned_data["date"])

    return render(request, "flights/list.html", {"form": form, "flights": flights})


def flight_detail(request, pk):
    flight = get_object_or_404(Flight, pk=pk)
    return render(request, "flights/detail.html", {"flight": flight})
