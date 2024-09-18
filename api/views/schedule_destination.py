from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from api.models.destination import Destination
from api.models.schedule import Schedule
from api.models.schedule_destination import ScheduleDestination
from api.serializers.schedule_destination import ScheduleDestinationSerializer
from api.utils.utils import calculate_average_weather, calculate_total_days, date_range, get_midpoint_date, get_weather_forecast


class ScheduleDestinationViewSet(viewsets.ModelViewSet):
    queryset = ScheduleDestination.objects.all()
    serializer_class = ScheduleDestinationSerializer

    def create(self, request, *args, **kwargs):
        schedule_id = request.data.get('schedule')
        destination_id = request.data.get('destination')
        arrival_date = request.data.get('arrival_date')
        departure_date = request.data.get('departure_date')
        
        if not all([schedule_id, destination_id, arrival_date, departure_date]):
            return Response({
                "message": "Schedule, destination, arrival_date, and departure_date are required.",
                "status": status.HTTP_400_BAD_REQUEST
            })
            
        schedule = get_object_or_404(Schedule, id=schedule_id)
        destination = get_object_or_404(Destination, id=destination_id)
        
        schedule_destination = ScheduleDestination.objects.create(
            schedule=schedule,
            destination=destination,
            arrival_date=arrival_date,
            departure_date=departure_date
        )
        
        serializer = self.get_serializer(schedule_destination)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def stay_info(self, request, pk=None):
        schedule_destination = self.get_object()
        destination = schedule_destination.destination
        start_date = schedule_destination.arrival_date
        end_date = schedule_destination.departure_date

        try:
            weather_data = []
            for date in date_range(start_date, end_date):
                daily_weather = get_weather_forecast(destination.latitude, destination.longitude, date)
                weather_data.append(daily_weather)

            average_weather = calculate_average_weather(weather_data)

            return Response({
                'destination': str(destination),
                'arrival_date': start_date,
                'departure_date': end_date,
                'duration': (end_date - start_date).days + 1,
                'average_weather': average_weather
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)