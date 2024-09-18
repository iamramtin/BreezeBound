from rest_framework import serializers

from api.models.destination import Destination


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ['id', 'city', 'country', 'latitude', 'longitude']

