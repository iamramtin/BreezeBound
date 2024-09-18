from django.db import models


class Destination(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        unique_together = ['city', 'country']

    def __str__(self):
        return f"{self.city}, {self.country}"
