from django.db import models


class Schedule(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    destinations = models.ManyToManyField('Destination', through='ScheduleDestination')

    def __str__(self):
        return f"{self.name} ({self.start_date.strftime("%Y-%m-%d")} to {self.end_date.strftime("%Y-%m-%d")})"