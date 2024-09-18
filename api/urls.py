from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views.destination import DestinationViewSet
from api.views.schedule import ScheduleViewSet
from api.views.schedule_destination import ScheduleDestinationViewSet

router = DefaultRouter()
router.register(r'destinations', DestinationViewSet)
router.register(r'schedules', ScheduleViewSet)
router.register(r'schedule-destinations', ScheduleDestinationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# Additional URL patterns for custom actions
urlpatterns += [
    path('schedules/<int:pk>/weather/', ScheduleViewSet.as_view({'get': 'weather'}), name='schedule-weather'),
]