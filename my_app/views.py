from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models

# Create your views here.

BASE_CRAIGLIST_URL = 'https://chennai.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'
def home(request):

    return render(request, 'base.html')


def new_search(request):

    search = request.POST.get('search')
    models.Search.objects.create(search = search)
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
            
            # add the image using the data-ids
        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'
            
        final_listing.append((post_title, post_url, post_price, post_image_url))
        
    push_to_frontend = {
        
        'search': search,
        'final_listing': final_listing
    }
    return render(request, 'my_app/new_search.html', push_to_frontend)
