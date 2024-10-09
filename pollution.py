import requests

def getLatLon(city, apikey):
   
    __url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=2&appid={apikey}"
    resp = requests.get(__url)
    if resp.status_code == 200:
        data = resp.json()
        if data:
            return data[0]["lat"], data[0]["lon"]
    return None

def getPollutionData(city, apikey):
   
    geoData = getLatLon(city, apikey)
    if geoData is None:
        return None

    lat, lon = geoData
    __url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={apikey}"
    resp = requests.get(__url)
    if resp.status_code == 200:
        data = resp.json()["list"][0]
        return {
            "aqi": data["main"]["aqi"],
            "pm2_5": data["components"]["pm2_5"],
            "pm10": data["components"]["pm10"],
            "o3": data["components"]["o3"],
            "no2": data["components"]["no2"],
            "so2": data["components"]["so2"],
            "co": data["components"]["co"]
        }
    return None

def getSuggestion(aqi):
    
    if aqi == 1:
        return "Air quality is good. You can go outside."
    elif aqi == 2:
        return "Air quality is fair. Outdoor activities are safe."
    elif aqi == 3:
        return "Air quality is moderate. Consider limiting outdoor activities."
    elif aqi == 4:
        return "Air quality is poor. Limit time spent outdoors and wear a mask."
    elif aqi == 5:
        return "Air quality is very poor. Avoid outdoor activities and wear a mask."
    return "AQI data is not available."
