from rest_framework import serializers

from api.models.schedule import Schedule
from api.serializers.schedule_destination import ScheduleDestinationSerializer


class ScheduleSerializer(serializers.ModelSerializer):
    schedule_destinations = ScheduleDestinationSerializer(source='scheduledestination_set', many=True, read_only=True)
    
    class Meta:
        model = Schedule
        fields = ['id', 'name', 'start_date', 'end_date', 'schedule_destinations']