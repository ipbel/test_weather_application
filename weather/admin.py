from django.contrib import admin

from weather.models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')

    fields = ['name', 'created', 'weather_data']
    readonly_fields = ['created',]
