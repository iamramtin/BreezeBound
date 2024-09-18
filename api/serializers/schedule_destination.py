from rest_framework import serializers

from api.models.schedule_destination import ScheduleDestination
from api.serializers.destination import DestinationSerializer


class ScheduleDestinationSerializer(serializers.ModelSerializer):
    destination = DestinationSerializer(read_only=True)
    
    class Meta:
        model = ScheduleDestination
        fields = ['id', 'destination', 'arrival_date', 'departure_date']
