from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.response import Response

from api.models.destination import Destination
from api.serializers.destination import DestinationSerializer
from api.utils.utils import get_coordinates


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    
    def create(self, request):
        city = request.data.get('city')
        country = request.data.get('country')

        latitude, longitude = get_coordinates(city, country)
        
        data = request.data.copy()
        data['latitude'] = latitude
        data['longitude'] = longitude
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except IntegrityError:
            return Response({
                "message": "A destination with this city and country already exists",
                "status": status.HTTP_400_BAD_REQUEST,
            })
            