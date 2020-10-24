from django.shortcuts import render,redirect
from .models import City
from .forms import CityForm
import requests
from django.contrib import messages


# Create your views here.
def index(request):
    API_key="96bf12f49a9878fe0c6c3b1f41fada4a"
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}"

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            #print(new_city)
            r = requests.get(url.format(new_city,API_key)).json()
            if r['cod'] == 200:
                if not City.objects.filter(name__iexact=new_city):
                    messages.success(request, "City added successfully")
                    form.save()
                else:
                    messages.error(request,"This city already exists")

            else:
                messages.error(request,"City does NOT exist")

            return redirect('index')
            
        

    form = CityForm()

    weather_data =[]
    cities = City.objects.all()
    for city in cities:
        r = requests.get(url.format(city.name,API_key)).json()
        city_weather = {
            'city': city.name,
            'temperature':r['main']['temp'],
            'description':r['weather'][0]['description'],
            'icon':r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)

    context={
        'weather_data': weather_data,
        'form': form,
    }


    return render(
        request=request,
        template_name = "weather/weather.html",
        context=context
    )
        
def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    messages.warning(request, f'{city_name} deleted!')
    return redirect ('index')