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
def fillMenuData(menu, itemURLs):
    menuData = []

    # Creates each item page and gets its name
    for i, j in zip(menu, itemURLs):
        infoPage = htmlToSoup(j)
        # nutriFacts = infoPage.find('table') TODO: pull table data

        # Assigns all the item's info from the lists
        foodObject = {
            "item": i,
            "calories": "",
            "serving": "",
            "fatCals": "",
            "fat": "",
            "satFat": "",
            "transFat": "",
            "cholesterol": "",
            "sodium": "",
            "carbs": "",
            "fiber": "",
            "sugar": "",
            "protein": ""
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

    # TODO: Creates calorie list; variable amounts are tagged as such
    cals = []
    calCount = menuPage.find('div', attrs={"class": "nutrition_button"}).get_text()
    print(calCount)

    # Creates itemURLs list with hrefs
    itemURLs = []
    for l in menuPage.findAll('a', attrs={"class": "listlink item_link active_item_link"}):
        itemURLs.append(base + l.get('href'))

    restaurantObject = {
        "link": base + href,
        "logo": logoURL,
        "name": name,
        "menu": [fillMenuData(menu, itemURLs)]
    }
    data.append(restaurantObject)

# Dumps the collected data into data.json
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
