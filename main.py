import os
import requests
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

# Fetch the API key from the environment variables
API_KEY = os.getenv('API_KEY')

# Base URL for OpenWeather API
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

def get_weather (city_name):
    """
    Fetches the weather data for a given city from the OpenWeatherMap API.

    Args:
        city_name (str): The name of the city to fetch weather data for.

    Returns:
        dict: The weather data returned from the API in JSON format, or None if an error occurs.
    """
    if API_KEY is None:
        print("API key not found.  Make sure it's set in the .env file.")
        return None
    
    request_url = f"{BASE_URL}?lat={lat}&lon={lon}&appid={API_KEY}"
# TODO: Need to call the Geocoding API to resolve the city name to lat / lon


