from datetime import timedelta

from django.db import models
from django.utils import timezone


def delete_old_entries():
    one_hour_ago = timezone.now() - timedelta(hours=1)
    City.objects.filter(created__lt=one_hour_ago).delete()


class City(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    weather_data = models.JSONField(default=dict)

    def __str__(self):
        return f'City: {self.name} - temp: {self.weather_data["temperature"]}°C'
