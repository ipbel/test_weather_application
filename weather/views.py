import requests
from deep_translator import GoogleTranslator
from django.shortcuts import render
from langdetect import detect

from weather.models import City, delete_old_entries
from weather_app.settings import API_KEY


def index(request):
    if request.method == 'GET':
        city = request.GET.get('city')
        if not city:
            return render(request, 'weather.html')

    # Проверка на ввод данных, если язык русский - переводим в английский и делаем запрос.
    try:
        if detect(city) == 'ru':
            city = GoogleTranslator(source='auto', target='en').translate(city)
    except Exception:
        error = 'languange type error'
        return render(request, 'weather.html', {'error': error})

    # Формирование запроса к openweathermap
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}&lang=ru'
    api_key = API_KEY
    response = requests.get(url.format(city, api_key))
    data = response.json()

    if response.status_code != 200:
        error = data['message']
        return render(request, 'weather.html', {'error': error})

    new_object = City.objects.create(
        name=city,
        weather_data={
            'temperature': round(data['main']['temp']),
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
        })

    current_weather = {
        'city': city,
        'created': new_object.created,
        **new_object.weather_data,
    }

    # Удаляем записи созданные более часа назад
    delete_old_entries()

    context = {
        'current_weather': current_weather,
        'cities_weather': City.objects.all().exclude(created=current_weather['created']).order_by('-created'),
    }
    return render(request, 'weather.html', context)
