from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models

# Create your views here.

BASE_CRAIGLIST_URL = 'https://chennai.craigslist.org/search/?query={}'

BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
def home(request):

    return render(request, 'base.html')


def new_search(request):

    search = request.POST.get('search')
    #models.Search.objects.create(search = search)
    print(search)
    # things to frontend
    final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
    #get response from site
    
    response = requests.get(final_url)
    data = response.text
    #initialise soup object wrapper for parsing
    soup = BeautifulSoup(data, features='html.parser')
    post_listings = soup.findAll('li', {'class': 'result-row'})# check for the li tag with result-row class for list of info
    
    
    final_listing = []
    
    for post in post_listings:
        #get the title, link and price
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'
        final_listing.append((post_title, post_url, post_price))

    push_to_frontend = {
        
        'search': search,
        'final_listing': final_listing
    }
    return render(request, 'my_app/new_search.html', push_to_frontend)
