from bs4 import BeautifulSoup as soup
import requests
from requests import Timeout
import json
import re

# Don't change this! This is the website we are pulling the restaurant names from.
basePage = 'https://fastfoodnutrition.org'
hubPage = 'https://fastfoodnutrition.org/fast-food-restaurants'

# Attempts a connection to the website. If the exception is thrown, the website is down (nothing we can do).
try:
    response = requests.get(
        hubPage, headers={'User-Agent': 'Mozilla/5.0'}, timeout=(2, 5))
except Timeout:
    print('Request timed out. Check server connection.')

# BeautifulSoup object representing the HTML contents
content = soup(response.content, "html.parser")
data = []

# Finds all <a> tags in the card view
for i in content.findAll('a', attrs={"class": "divider"}):
    restaurantObject = {
        "link": hubPage + i.get('href'),
        "name": i.get('href')[1:]
    }
    data.append(restaurantObject)

# Dumps the collected data into data.json
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)

#images = content.findAll('div', attrs={"class": "logo_box_image lozad"})

print(response)  # HTTP Status code for debugging purposes
#print(names)
#print(images)
#print (restaurants)
