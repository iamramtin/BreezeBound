from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from api.models.schedule import Schedule
from api.serializers.schedule import ScheduleSerializer
from api.utils.utils import date_range, get_schedule_summary, get_weather_forecast


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    
    @action(detail=True, methods=['get'])
    def weather(self, requests, pk=None):
        schedule = self.get_object()
        forecast = []
        
        for schedule_destination in schedule.scheduledestination_set.all():
            destination = schedule_destination.destination
            for date in date_range(schedule_destination.arrival_date, schedule_destination.departure_date):
                weather = get_weather_forecast(destination.latitude, destination.longitude, date)
                forecast.append({
                    'destination': str(destination),
                    'date': date,
                    'weather': weather
                })
        return Response(forecast)

    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        schedule = self.get_object()
        summary = get_schedule_summary(schedule)
        return Response(summary)
