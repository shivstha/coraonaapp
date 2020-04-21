from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from . import models


# Create your views here.

BASE_URL = 'https://www.worldometers.info/coronavirus'
BASE_URL_COUNTRY = 'https://www.worldometers.info/coronavirus/country/{}'
FLAG_URL = 'https://www.worldometers.info/{}'


def home(request):
    response = requests.get(BASE_URL)
    data = response.text
    soup1 = BeautifulSoup(data, features='html.parser')
    cases_corona = soup1.find_all('div', {'class': 'maincounter-number'})
    spread = cases_corona[0].find('span').text
    deaths = cases_corona[1].find('span').text
    recover = cases_corona[2].find('span').text
    total_case = [spread, deaths, recover]
    context = {
        'cases': total_case
    }
    return render(request, 'home.html', context)


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    if search.lower() == 'usa' or search.lower() == "united states" or search.lower() == "america" or search.lower() == "united states of america":
        search = 'us'
    if search.lower() == 'united kingdom' or search.lower() == 'britain':
        search = 'uk'
    try:
        final_url_country = BASE_URL_COUNTRY.format('-'.join(search.split()))
        response = requests.get(final_url_country)
        data = response.text
        soup2 = BeautifulSoup(data, features='html.parser')
        cases_corona = soup2.find_all('div', {'class': 'maincounter-number'})
        country_img = soup2.find('div', {'style': 'display:inline'}).find('img').get('src')
        final_img = FLAG_URL.format(country_img)
    except:
        return render(request, 'invalid_name.html', {'country_name': search})
    else:
        spread = cases_corona[0].find('span').text
        deaths = cases_corona[1].find('span').text
        recover = cases_corona[2].find('span').text
        total_case_country = [spread, deaths, recover]
        context = {
            'cases': total_case_country,
            'country_name': search.upper(),
            'final_img': final_img
        }
        return render(request, 'new_search.html', context)


