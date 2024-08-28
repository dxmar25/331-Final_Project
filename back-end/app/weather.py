import requests
import time

# current weather info https://openweathermap.org/current

# need ['coord','weather','base','main','wind','visibility']

API_KEY = "8b9d48ac8ce58965eea3d5fa09bf1a7f"

params = {
    "lat": "30.612541",
    "lon": "-96.3433166",
    "dt": str(int(time.time())),
    "appid": API_KEY,
    "units": "imperial",
}


weatherData = {}  # empty initialization


# run at start of each function
def getCurrentInfo():
    global weatherData
    params["dt"] = str(int(time.time()))
    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather?", params=params
    )
    weatherData = response.json()
    print(weatherData)


# assumes getCurrentInfo has been run
def getTemperature():
    # print(weatherData)
    return weatherData["main"]["temp"]


def getWeatherIcon():
    return weatherData["weather"][0]["icon"]


# TODO: weather descriptions from website https://openweathermap.org/weather-conditions
def getWeatherConditionName():
    # weather conditions based on id
    conditionName = "Unknown"
    conditionNumber = str(weatherData["weather"][0]["id"])[0]  # 2,3,4,5
    if weatherData["weather"][0]["id"] == "800":
        return "Clear"

    if conditionNumber == "2":
        conditionName = "Thunderstorm"
    if conditionNumber == "3":
        conditionName = "Drizzle"
    if conditionNumber == "5":
        conditionName = "Rain"
    if conditionNumber == "6":
        conditionName = "Snow"  # highly improbable
    if conditionNumber == "7":
        conditionName = "Obscure"
    if conditionNumber == "8":
        conditionName = "Cloudy"

    return conditionName


# TODO: surge pricing conditions


# Combine all useful data and put here (for main api call)
def getAggregateData():
    getCurrentInfo()
    data = {
        "temperature": getTemperature(),
        "icon": getWeatherIcon(),  # icon
        "condition": getWeatherConditionName(),
        "surge": getSurgePricing(),
    }
    return data


"""
Surge pricing formula
Burgers
Baskets
Shakes n Sweets (1.25x price if temp greater than 80, 1.5x if greater than 90, 2x if greater than 100)
Sandwiches
Beverages (1.25x price if temp greater than 80, 1.5x if greater than 90, 2x if greater than 100)
Sides (1.25x)
Sauces

if "thunderstorm" 2x everything on top of existing multiplier
if rain 1.25x on everything

if 
"""


def getSurgePricing():
    # assgumes latest data
    surgeDefault = 1.1
    surgeCategories = {
        "Burgers": surgeDefault,
        "Baskets": surgeDefault,
        "ShakesnSweets": surgeDefault,
        "Sandwiches": surgeDefault,
        "Beverages": surgeDefault,
        "Sides": surgeDefault,
        "Sauces": surgeDefault,
    }
    temp = getTemperature()
    if temp > 100:
        surgeCategories["ShakesnSweets"] *= 2
        surgeCategories["Beverages"] *= 2
    elif temp > 90:
        surgeCategories["ShakesnSweets"] *= 1.5
        surgeCategories["Beverages"] *= 1.5
    elif temp > 80:
        surgeCategories["ShakesnSweets"] *= 1.25
        surgeCategories["Beverages"] *= 1.25

    if getWeatherConditionName() == "Thunderstorm":
        for i in surgeCategories:
            surgeCategories[i] *= 2
    elif getWeatherConditionName() == "Rain":
        for i in surgeCategories:
            surgeCategories[i] *= 1.25

    return surgeCategories


# DEBUG
if __name__ in "__main__":
    getCurrentInfo()
    print(getAggregateData())
