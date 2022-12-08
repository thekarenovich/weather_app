import requests
from django.http import HttpResponse
from django.shortcuts import render

from .models import City
from .forms import CityForm


def index(request):
    b = True
    appid = '294a22111fcea5b6e6fd83c963faf8e4'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()
    cities = City.objects.all()
    all_cities = ['']

    if City.objects.count() > 0:
        city = cities[len(cities) - 1].name

    else:
        city = 'London'

    res = requests.get(url.format(city)).json()

    if res['cod'] == 200:
        city_info = {
            'country': res['sys']['country'],
            'city': city,
            'temp': res['main']['temp'],
            'icon': res['weather'][0]['icon']
        }
        all_cities[0] = city_info
        b = True
    else:
        b = False

    context = {'all_info': all_cities, 'form': form, 'b': b}

    return render(request, "weather/index.html", context)
