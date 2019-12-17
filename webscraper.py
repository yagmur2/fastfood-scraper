from bs4 import BeautifulSoup
import requests
from requests import Timeout
import json
import time

# Don't change this! This is the website we are pulling the restaurant names from.
base = 'https://fastfoodnutrition.org'
hub = 'https://fastfoodnutrition.org/fast-food-restaurants'
data = []  # JSON data dump list


# Sends a request to the website, then converts the HTML response to BeautifulSoup structure.
# If the exception is thrown, the website is refusing connection (nothing we can do).
def htmlToSoup(website):
    response = ''
    while response == '':
        try:
            response = requests.get(
                website, headers={'User-Agent': 'Mozilla/5.0'}, timeout=(2, 5))
            break
        except ConnectionError:
            print("Connection refused by the server...")
            print("Trying again in 5 seconds...")
            time.sleep(5)
            print("Attempting connection again...")
            continue
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


# Helper method that fills foodObject JSON data from each store's menu.
# Creates an empty list, goes to each food's page, and fills the list.
def fillMenuData(menu, itemLinks):
    menuData = []

    # Creates each item page and gets its name
    for i, j in zip(itemLinks, menu):
        infoPage = htmlToSoup(i)
        print(i)  # debug
        print(j)  # debug
        # Assigns all the item's info from the lists
        for k in infoPage.findAll("table", attrs={"class": "item_itemtion"}):
            foodObject = {
                "item": j,
                "calories": "",
                "serving": "",
                "fatCals": "",
                "fat": ""
            }
            menuData.append(foodObject)
    return menuData

hubPage = htmlToSoup(hub)

# Loops through each restaurant page, assigning a fresh set of variables for each.
for i in hubPage.findAll('a', attrs={"class": "divider"}):
    href = i.get('href')
    menuPage = htmlToSoup(base + href)
    logoURL = base + menuPage.find('img', attrs={"class": "logo_float"})['src']
    name = menuPage.find('h3').text

    # Creates menu list with names
    menu = []
    for j in menuPage.findAll('div', attrs={"class": "filter_target"}):
        menu.append(j.get('title'))

    # Creates itemLinks list with item URLs
    itemLinks = []
    for k in menuPage.findAll('a', attrs={"class": "listlink item_link active_item_link"}):
        itemLinks.append(base + k.get('href'))

    restaurantObject = {
        "link": base + href,
        "logo": logoURL,
        "name": name,
        "menu": fillMenuData(menu, itemLinks)
    }
    data.append(restaurantObject)

# Dumps the collected data into data.json
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
