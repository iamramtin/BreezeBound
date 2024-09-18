from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date

from api.models.destination import Destination
from api.models.schedule import Schedule
from api.models.schedule_destination import ScheduleDestination


class DestinationModelTest(TestCase):
    def test_destination_creation(self):
        destination = Destination.objects.create(
            city="Paris",
            country="France",
            latitude=48.8566,
            longitude=2.3522
        )
        self.assertEqual(str(destination), "Paris, France")


class ScheduleModelTest(TestCase):
    def test_schedule_creation(self):
        schedule = Schedule.objects.create(
            name="Summer Vacation",
            start_date=date(2024, 7, 1),
            end_date=date(2024, 7, 14)
        )
        self.assertEqual(str(schedule), "Summer Vacation (2024-07-01 to 2024-07-14)")


class ScheduleDestinationModelTest(TestCase):
    def setUp(self):
        self.schedule = Schedule.objects.create(
            name="Summer Vacation",
            start_date=date(2024, 7, 1),
            end_date=date(2024, 7, 14)
        )
        self.destination = Destination.objects.create(
            city="Paris",
            country="France",
            latitude=48.8566,
            longitude=2.3522
        )


    def test_valid_schedule_destination(self):
        schedule_destination = ScheduleDestination(
            schedule=self.schedule,
            destination=self.destination,
            arrival_date=date(2024, 7, 2),
            departure_date=date(2024, 7, 5)
        )
        schedule_destination.full_clean()  # Should not raise ValidationError


    def test_invalid_date_range(self):
        with self.assertRaises(ValidationError):
            schedule_destination = ScheduleDestination(
                schedule=self.schedule,
                destination=self.destination,
                arrival_date=date(2024, 7, 5),
                departure_date=date(2024, 7, 2)
            )
            schedule_destination.full_clean()
