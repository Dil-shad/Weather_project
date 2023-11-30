from django.urls import path
from .views import weather_forecast_lookup

urlpatterns = [
    path('', weather_forecast_lookup, name="weather_forecast")
]
