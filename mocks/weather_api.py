import requests

def get_weather(city):
    # Simulate an API call to an EXTERNAL api
    response = requests.get(f"http://api.weather.com/v1/{city}")
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError("Could not fetch weather data")