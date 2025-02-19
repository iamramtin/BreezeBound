from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException

class GeolocationError(APIException):
    status_code = 400
    default_detail = 'Failed to get geolocation.'
    default_code = 'geolocation_error'

class WeatherForecastError(APIException):
    status_code = 400
    default_detail = 'Failed to get weather forecast.'
    default_code = 'weather_forecast_error'

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        response.data['status_code'] = response.status_code
    
    return response