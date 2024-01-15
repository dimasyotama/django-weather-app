import requests
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from .forms import CityForm
from .models import city
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from decouple import config


def index(request):
    """
    Render the weather index page, allowing users to add and view weather data for different cities.

    Parameters:
        request (HttpRequest): The Django HttpRequest object.

    Returns:
        HttpResponse: The rendered weather index page.

    Raises:
        None

    Usage:
        This view function handles both GET and POST requests. For GET requests, it renders the weather
        index page with a form for adding cities and a list of existing cities with their weather data.
        For POST requests, it processes the submitted form, adds the city to the database if it doesn't
        already exist, and updates the weather data for all cities.

    """

    new_city, url, token_key = None, '', config('TOKEN_KEY', '')
    err_msg, message, message_class = '', '', ''
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            url = f'http://api.openweathermap.org/data/2.5/weather?q={new_city}&units=metric&appid={token_key}'
            existing_city_count = city.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(url).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = "City doesnt exist"
            else:
                err_msg = "City already exist in the database!"
        if err_msg :
            message = err_msg
            message_class = 'alert-danger'
        else:
            message = 'City added successfully!'
            message_class = "alert-success"
    
    form = CityForm()
    cities = city.objects.all()

    weather_data = []

    for citi in cities:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={citi}&units=metric&appid={token_key}'
        r = requests.get(url).json()
        city_weather  = {
            'city' : citi.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {
        'weather_data' : weather_data, 
        'form':form,
        'message':message,
        'message_class':message_class
    }

    return render(request, 'weather/weather.html',context)

def about(request) :
    """
    Render the about page.

    Parameters:
        request (HttpRequest): The Django HttpRequest object.

    Returns:
        HttpResponse: The rendered about page.

    Raises:
        None

    Usage:
        This view function handles GET requests and renders the about page.

    """
     
    return render(request,'weather/about.html')

    
def delete_city(request, city_name):
    """
    Delete a city from the database.

    Parameters:
        request (HttpRequest): The Django HttpRequest object.
        city_name (str): The name of the city to be deleted.

    Returns:
        HttpResponseRedirect: Redirects to the home page after deleting the city.

    Raises:
        DoesNotExist: If the specified city does not exist in the database.

    Usage:
        This view function handles GET requests and deletes the specified city from the database.
        After deletion, it redirects the user to the home page.

    """
    city.objects.get(name=city_name).delete()
    return redirect('home')

def help(request):
    """
    Render the help page.

    Parameters:
        request (HttpRequest): The Django HttpRequest object.

    Returns:
        HttpResponse: The rendered help page.

    Raises:
        None

    Usage:
        This view function handles GET requests and renders the help page.

    """
    return render(request,'weather/help.html')
