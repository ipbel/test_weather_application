from django.urls import path

from weather.views import index

urlpatterns = [
    path('', index, name='index'),
]
