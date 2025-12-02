from django.urls import path
from .views import flight_list, flight_detail

app_name = "flights"

urlpatterns = [
    path("", flight_list, name="list"),
    path("<int:pk>/", flight_detail, name="detail"),
]