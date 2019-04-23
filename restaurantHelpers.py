from random import randrange
import json
restaurants = []
saveFile = '/home/ubuntu/lunchbot/restaurantData.json'

def alreadyAdded(restaurantName):
    for restaurant in restaurants:
        if(restaurant['name'] == restaurantName):
            return True
    return False

def addRestaurant(restaurantName):
    global restaurants
    restaurants.insert(0, {'name': restaurantName, 'weight': 1})
    saveToFile()

def incrementWeights():
    global restaurants
    for i in range(len(restaurants)):
        restaurants[i]['weight'] += 1
    saveToFile()

def removePriority(restaurantName):
    global restaurants
    for i in range(len(restaurants)):
        if(restaurants[i]['name'] == restaurantName):
            restaurants[i]['weight'] = 0
            saveToFile()
            return

def removeRestaurant(restaurantName):
    global restaurants
    for i in range(len(restaurants)):
        if(restaurants[i]['name'] == restaurantName):
            restaurants.remove(restaurants[i])
            saveToFile()
            return True
    return False

def chooseRandomRestaurant():
    global restaurants
    total = 0
    for restaurant in restaurants:
        total += restaurant['weight']
    choice = randrange(total)
    total = 0
    for i in range(len(restaurants)):
        if(choice < restaurants[i]['weight']):
            return restaurants[i]['name']
        else:
            choice -= restaurants[i]['weight']
    return "No Where"

def getRestaurantList():
    global restaurants
    table = '"#### Restaurant List\\n|Restaurant|Weight|\\n|:---|:---|'
    for restaurant in restaurants:
        table += "\\n|{location}|{level}|".format(
            location=restaurant['name'], level=restaurant['weight'])
    table += '\\n"'
    return table

def readRestaurantsFromFile():
    global restaurants, saveFile
    try:
        file = open(saveFile, 'r')
        restaurants = json.loads(file.read())
    except:
        print("failed to load from file; creating new restaurant array")
        restaurants = []


def saveToFile():
    global restaurants, saveFile
    file = open(saveFile, 'w')
    file.write(json.dumps(restaurants))
    file.close()
