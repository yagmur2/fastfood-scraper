from bs4 import BeautifulSoup
import requests
from requests import Timeout
import json
import re

# Don't change this! This is the website we are pulling the restaurant names from.
base = 'https://fastfoodnutrition.org'
hub = 'https://fastfoodnutrition.org/fast-food-restaurants'
data = [] # JSON data dump list

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

hubPage = htmlToSoup(hub)

# Loops through each restaurant page, assigning a fresh set of variables for each.
for i in hubPage.findAll('a', attrs={"class": "divider"}):
    href = i.get('href')
    menuPage = htmlToSoup(base + href)
    logoURL = base + menuPage.find('img', attrs={"class": "logo_float"})['src']
    name = menuPage.find('h3').text
    menu = []
    cals = []

    # Fills menu list
    for k in menuPage.findAll('u', attrs={"class": "rest_item_list"}):
        menu.append(k.get('title'))
        foodItem = htmlToSoup()

    restaurantObject = {
        "link": base + href,
        "logo": logoURL,
        "name": name,
        "menu": menu
    }
    data.append(restaurantObject)

# Dumps the collected data into data.json
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)