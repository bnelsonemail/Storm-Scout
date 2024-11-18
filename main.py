"""Main.py."""

import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Weather:
    """
    Class that uses an API call to collect weather data based on user input of
    City, State Code, and Country Code (e.g., US, GB, etc.)
    """

    def __init__(self, city_name_param, state_code_param, country_code):
        self._api_key = os.getenv('API_KEY')
        self.base_geocode_url = 'http://api.openweathermap.org/geo/1.0/direct'
        self.base_weather_url = 'https://api.openweathermap.org/data/2.5/weather'
        self.base_radar_url = 'http://api.openweathermap.org/data/3.0/onecall'
        self.city_name = city_name_param
        self.state_code = state_code_param
        self.country_code = country_code

        if not self._api_key:
            raise ValueError("API key not found. Please set the API key in the"
                             ".env file")

    def get_lat_lon(self):
        """
        Retrieve the latitude and longitude for a specified location.

        This method sends a GET request to the geocoding API using the
        provided city, state, and country codes. It extracts and returns
        the latitude and longitude of the location.

        Returns:
            tuple: A tuple containing the latitude and longitude as floats,
                e.g., (37.7749, -122.4194).
            None: If the location data is unavailable or an error occurs.

        Raises:
            requests.RequestException: If there is an error in the API
                request or response.

        Example:
            >>> lat, lon = get_lat_lon()
            >>> print(f"Latitude: {lat}, Longitude: {lon}")
        """
        params = {
            'q': f'{self.city_name},{self.state_code},{self.country_code}',
            'limit': 1,
            'appid': self._api_key
        }

        try:
            response = requests.get(self.base_geocode_url, params=params,
                                    timeout=10)
            response.raise_for_status()
            data = response.json()

            if data:
                latitude = float(data[0]['lat'])
                longitude = float(data[0]['lon'])
                return latitude, longitude
            else:
                print("No location data found.")
                return None
        except requests.RequestException as e:
            print(f"Error fetching latitude and longitude data: {e}")
            return None

    def get_weather(self, latitude, longitude):
        """
        Fetch the current weather data for a specified location.

        This method sends a GET request to the weather API with
        the provided latitude and longitude, retrieves the weather
        data, and returns it in JSON format.

        Args:
            latitude (float): The latitude of the location for
                which to fetch the weather.
            longitude (float): The longitude of the location for
                which to fetch the weather.

        Returns:
            dict: A dictionary containing the weather data if the
                request is successful.
            None: If an error occurs during the API request or
                response parsing.

        Raises:
            requests.exceptions.HTTPError: If the response contains
                an HTTP error status code.
            requests.exceptions.RequestException: If a network-related
                error occurs during the request.
            ValueError: If the response cannot be decoded into JSON
                format.

        Example:
            >>> weather = get_weather(37.7749, -122.4194)
            >>> if weather:
            ...     print(weather["main"]["temp"])  # Prints the temp
        """
        params = {
            'lat': latitude,
            'lon': longitude,
            'appid': self._api_key,
            'units': 'imperial'
        }

        try:
            response = requests.get(self.base_weather_url, params=params,
                                    timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
        except ValueError as val_err:
            print(f"Value error occurred: {val_err}")

        return None

    def get_radar_map(self, latitude, longitude):
        """
        Fetches the radar map URL for the specified latitude and longitude.

        Args:
            latitude (float): Latitude of the location.
            longitude (float): Longitude of the location.

        Returns:
            str: URL of the radar map.
        """
        params = {
            'lat': latitude,
            'lon': longitude,
            'appid': self._api_key,
            'zoom': 10,  # Zoom level for the radar map
            # Example overlay; customize as needed
            'overlay': 'precipitation_new'
        }

        try:
            radar_response = requests.get(self.base_radar_url, params=params,
                                          timeout=10)
            radar_response.raise_for_status()
            radar_data = radar_response.json()
            # Assuming the radar URL is in the response; customize based on
            # actual API response
            # Adjust this based on actual response structure
            return radar_data['radar_url']
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred while fetching radar map: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred while fetching radar map: "
                  f"{req_err}")
        except ValueError as val_err:
            print(f"Value error occurred while fetching radar map: {val_err}")

        return None

    def display_weather(self, weather_info, location_info):
        """
        Display weather details for a given location.

        Args:
            weather_info (dict): A dictionary containing weather
                data such as temperature, humidity, wind speed,
                and pressure.
            location_info (tuple): A tuple containing the city and
                state for the location (city, state).

        Prints:
            Weather details including temperature, feels-like
            temperature, condition, humidity, wind speed, and
            pressure. If no weather data is provided, a message
            is displayed stating that data is unavailable.

        Example:
            >>> display_weather(weather_info, ("San Francisco", "CA"))
            Weather in San Francisco, CA:
            Temperature: 72°F
            Feels Like Temperature: 75°F
            Condition: Clear sky
            Humidity: 60 %
            Wind Speed: 5 mph
            Pressure: 1015 hPa
        """
        if weather_info:
            temp = weather_info['main']['temp']
            feels_like = weather_info['main']['feels_like']
            description = weather_info['weather'][0]['description']
            humidity = weather_info['main']['humidity']
            wind = weather_info['wind']['speed']
            pressure = weather_info['main']['pressure']
            loc_city, loc_state = location_info

            print(f"\nWeather in {loc_city}, {loc_state}:")
            print(f"Temperature: {temp}°F")
            print(f"Feels Like Temperature: {feels_like}°F")
            print(f"Condition: {description.capitalize()}")
            print(f"Humidity: {humidity} %")
            print(f"Wind Speed: {wind} mph")
            print(f"Pressure: {pressure} hPa")
        else:
            print("No weather data available.")


if __name__ == "__main__":
    city = input("Enter the city name: ")
    state_code = input("Enter the state code "
                       "(optional, press Enter to skip): ")
    country = input("Enter the country code: ")

    weather = Weather(city, state_code, country)
    lat_lon = weather.get_lat_lon()

    if lat_lon:
        lat, lon = lat_lon
        weather_data = weather.get_weather(lat, lon)
        weather.display_weather(weather_data, (city, state_code))

        radar_url = weather.get_radar_map(lat, lon)
        if radar_url:
            print(f"Radar map URL: {radar_url}")
