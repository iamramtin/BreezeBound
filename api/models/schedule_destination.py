from django.db import models
from django.core.exceptions import ValidationError

from api.utils.utils import is_date_in_range, validate_date_range


class ScheduleDestination(models.Model):
    schedule = models.ForeignKey('Schedule', on_delete=models.CASCADE)
    destination = models.ForeignKey('Destination', on_delete=models.CASCADE)
    arrival_date = models.DateField()
    departure_date = models.DateField()

    class Meta:
        ordering = ['arrival_date']
        
    def __str__(self):
        destination_name = f"{self.destination.city}, {self.destination.country}"
        return f"{self.schedule.name} - {destination_name} ({self.arrival_date} to {self.departure_date})"

    def clean(self):
        validate_date_range(self.arrival_date, self.departure_date)
        if not is_date_in_range(self.arrival_date, self.schedule.start_date, self.schedule.end_date) or \
           not is_date_in_range(self.departure_date, self.schedule.start_date, self.schedule.end_date):
            raise ValidationError("Destination dates must be within the schedule's date range.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)