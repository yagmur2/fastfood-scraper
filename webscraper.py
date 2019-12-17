from bs4 import BeautifulSoup
import requests
from requests import Timeout
import json
import re

# Don't change this! This is the website we are pulling the restaurant names from.
basePage = 'https://fastfoodnutrition.org'
hubPage = 'https://fastfoodnutrition.org/fast-food-restaurants'

# Sends a request to the website, then converts the HTML response to BeautifulSoup structure.
# If the exception is thrown, the website is down (nothing we can do).


def htmlToSoup(website):
    try:
        response = requests.get(
            website, headers={'User-Agent': 'Mozilla/5.0'}, timeout=(2, 5))
        # print(response) #--used for debugging
    except Timeout:
        print('Request timed out. Check server connection.')
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


hub = htmlToSoup(hubPage)
data = []

# Finds all <a> tags in the card view
for i in hub.findAll('a', attrs={"class": "divider"}):
    href = i.get('href')

    restaurantObject = {
        "link": hubPage + href,
        "name": href[1:].capitalize()
    }
    data.append(restaurantObject)

# Dumps the collected data into data.json
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)

#images = content.findAll('div', attrs={"class": "logo_box_image lozad"})
