import os
import requests
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()


class Weather:
    """
    Class that uses an API call to collect weather data based on user input of City, State Code and Country Code (ie: US, GB, etc.)
    """
    
    def __init__(self, city_name, state_code, limit, lang, country_code):
        """
        Initializes the Weather class with city name, state code, and country code.

        Args:
            city_name (str): Name of the city.
            state_code (str): State code (optional, can be an empty string if not applicable).
            country_code (str): Country code (ISO 3166 country codes).
        """
        self._api_key = os.getenv('API_KEY')
        self.base_geocode_url = 'http://api.openweathermap.org/geo/1.0/direct'
        self.base_weather_url = 'https://api.openweathermap.org/data/2.5/weather'
        self.city_name = city_name
        self.state_code = state_code
        self.country_code = country_code
        self.limit = limit,
        self.lang = lang


    def get_lat_lon(self):
        """
        Fetches latitude and longitude for the given city and state using the Zippopotam.us API.

        Returns:
            tuple: A tuple containing latitude and longitude if successful, None if there's an error.
        """
        # Format city and state for the URL
        city_formatted = self.city_name.replace(" ", "%20").lower()
        state_formatted = self.state_code.lower()

        # Build the Zippopotam.us API request
        url = f"http://api.zippopotam.us/us/{state_formatted}/{city_formatted}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data['places']:
                # Extract the first place's latitude and longitude
                lat = float(data['places'][0]['latitude'])
                lon = float(data['places'][0]['longitude'])
                return lat, lon
            else:
                print("No location data found.")
                return None
        except requests.RequestException as e:
            print(f"Error fetching latitude and longitude data: {e}")
            return None

    
    def get_weather (self, lat, lon):
        """
        Fetches the weather data from the OpenWeatherMap API using latitude and longitude.

        Args:
            lat (float): Latitude of the location.
            lon (float): Longitude of the location.

        Returns:
            dict: The weather data returned from the API in JSON format, or None if an error occurs.
        """

        params = {
            'lat': lat,
            'lon': lon,
            'appid': self._api_key,
            'units': 'standard'
        }
    
        try:
            response = requests.get(self.base_weather_url, params=params)
            response.raise_for_status() # Raises an error if the request was unsuccessful
            return response.json()
        except requests.exeptions.GTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Error occurred: {err}")
        
        return None
    
    
    def display_weather(self, weather_data, location_info):
        """
        Displays the weather information fetched from the API.

        Args:
            weather_data (dict): The weather data returned from the API.
            location_info (tuple): A tuple containing location details (name, state, country).
        """      
        if weather_data:
            temp = weather_data['main']['temp']
            description = weather_data['weather'][0]['description']
            city, state = location_info
            
            print(f"\nWeather in {city}, {state}:")
            print(f"Temperature: {temp}°F")
            print(f"Condition: {description.capitalize()}")
        else:
            print("No wather data available.")
        

    
if __name__ == "__main__":
    # Get user input for city, state, and country
    city_name = input("Enter the city name: ")
    state_code = input("Enter the state code (optional, press Enter to skip): ")
    country_code = input("Enter the country code: ")

    # Create a Weather object
    weather = Weather(city_name, state_code, country_code)
    
    # Get the latitude and longitude
    lat_lon = weather.get_lat_lon()
    
    if lat_lon:
        lat, lon = lat_lon
        # Fetch and display weather
        weather_data = weather.get_weather(lat, lon)
        weather.display_weather(weather_data, (city_name, state_code))