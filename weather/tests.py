from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from weather.models import City


class WeatherTests(TestCase):

    def test_view(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_creation_data(self):
        data = City.objects.create(
            name="Mogilev",
            weather_data={
                "humidity": 64,
                "description": "Ясно",
                "temperature": 5,
            }
        )
        self.assertEqual(data.name, "Mogilev")
        self.assertEqual(data.weather_data["humidity"], 64)
        self.assertEqual(data.weather_data["description"], "Ясно")
        self.assertEqual(data.weather_data["temperature"], 5)

    def test_api(self):
        response = self.client.get('/?city=Grodno')
        print(response.content)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Weather in')
        response = self.client.get('/?city=London')
        self.assertContains(response, 'History of weather requests')
