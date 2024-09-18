from datetime import timedelta
from django.core.exceptions import ValidationError
import requests

from api.utils.errors import GeolocationError, WeatherForecastError


WEATHER_API_URL = "https://api.open-meteo.com/v1"
GEOCODING_API_URL = "https://nominatim.openstreetmap.org"

def date_range(start_date, end_date):
    """
    Generate a range of dates from start_date to end_date (inclusive).
    """
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def is_date_in_range(date, start_date, end_date):
    """
    Check if a given date is within a date range (inclusive).
    """
    return start_date <= date <= end_date


def validate_date_range(start_date, end_date):
    """
    Validate that start_date is before or equal to end_date.
    """
    if start_date > end_date:
        raise ValidationError("Start date must be before or equal to end date.")


def get_overlapping_dates(range1_start, range1_end, range2_start, range2_end):
    """
    Get the overlapping dates between two date ranges.
    Returns None if there's no overlap.
    """
    latest_start = max(range1_start, range2_start)
    earliest_end = min(range1_end, range2_end)
    
    if latest_start <= earliest_end:
        return latest_start, earliest_end
    return None


def calculate_total_days(start_date, end_date):
    """
    Calculate the total number of days in a date range (inclusive).
    """
    return (end_date - start_date).days + 1


def get_midpoint_date(start_date, end_date):
    """
    Get the midpoint date between start_date and end_date.
    """
    total_days = calculate_total_days(start_date, end_date) - 1 # exclusive
    return start_date + timedelta(days=total_days // 2)


def get_schedule_summary(schedule):
    """
    Generate a comprehensive summary of a schedule, including total days,
    destinations, and stay durations.
    """
    total_days = calculate_total_days(schedule.start_date, schedule.end_date)
    destinations = schedule.schedule_destinations.all().order_by('arrival_date')
    
    summary = {
        'name': schedule.name,
        'total_days': total_days,
        'start_date': schedule.start_date,
        'end_date': schedule.end_date,
        'destinations': [],
        'travel_days': 0
    }
    
    previous_departure = schedule.start_date - timedelta(days=1)
    
    for dest in destinations:
        stay_duration = calculate_total_days(dest.arrival_date, dest.departure_date)
        travel_days = (dest.arrival_date - previous_departure).days - 1
        
        summary['destinations'].append({
            'city': dest.destination.city,
            'country': dest.destination.country,
            'arrival_date': dest.arrival_date,
            'departure_date': dest.departure_date,
            'stay_duration': stay_duration
        })
        
        summary['travel_days'] += travel_days
        previous_departure = dest.departure_date
    
    # Calculate days spent at destinations
    days_at_destinations = sum(dest['stay_duration'] for dest in summary['destinations'])
    
    # Calculate any remaining travel days after the last destination
    if previous_departure < schedule.end_date:
        summary['travel_days'] += (schedule.end_date - previous_departure).days
    
    summary['days_at_destinations'] = days_at_destinations
    summary['free_days'] = total_days - days_at_destinations - summary['travel_days']
    
    return summary


def get_coordinates(city, country):
    """
    Get the latitude and longitude values for a location.
    """
    params = {
        "city": city,
        "country": country,
        "format": "json"
    }
    headers = {
        "User-Agent": f"BreezeBound/1.0"
    }
    try:
        response = requests.get(f"{GEOCODING_API_URL}/search", params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data:
            return (float(data[0]["lat"]), float(data[0]["lon"]))
        else:
            raise GeolocationError(f"No coordinates found for {city}, {country}")
    except requests.RequestException as e:
        raise GeolocationError(f"Geocoding API error: {str(e)}")


def calculate_average_weather(weather_data):
    if not weather_data:
        return None

    total_max_temp = sum(day['max_temp'] for day in weather_data)
    total_min_temp = sum(day['min_temp'] for day in weather_data)
    total_precipitation = sum(day['precipitation'] for day in weather_data)
    days = len(weather_data)

    return {
        'avg_max_temp': round(total_max_temp / days, 1),
        'avg_min_temp': round(total_min_temp / days, 1),
        'avg_precipitation': round(total_precipitation / days, 1)
    }


def get_weather_forecast(latitude, longitude, date):
    """
    Get the weather forecast for a location.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "GMT",
        "start_date": date.strftime("%Y-%m-%d"),
        "end_date": date.strftime("%Y-%m-%d")
    }
    
    try:
        response = requests.get(f"{WEATHER_API_URL}/forecast", params=params)
        response.raise_for_status()
        data = response.json()
        
        daily = data['daily']
        
        return {
            "max_temp": daily['temperature_2m_max'][0],
            "min_temp": daily['temperature_2m_min'][0],
            "precipitation": daily['precipitation_sum'][0]
        }
    except requests.RequestException as e:
        raise WeatherForecastError(f"Weather API error: {str(e)}")
