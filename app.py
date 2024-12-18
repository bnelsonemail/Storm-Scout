from flask import Flask, render_template, request, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from config import DevelopmentConfig  # Use DevelopmentConfig, TestingConfig or ProductionConfig
from dotenv import load_dotenv, find_dotenv
import os
from main import Weather

# Load environment variables from the .env file
load_dotenv(find_dotenv())

app = Flask(__name__)

# Call config files
app.config.from_object(DevelopmentConfig)  # Use DevelopmentConfig, TestingConfig or ProductionConfig
debug = DebugToolbarExtension(app)

# ********************  ROUTING *******************************************

@app.route('/')
def home():
    """Renders the home page."""
    return render_template('home.html')


@app.route('/form', methods=['GET', 'POST'])
def form():
    """Renders the form and displays weather results if available."""
    if request.method == 'POST':
        city = request.form.get('city').lower()
        state = request.form.get('state').upper()
        country = request.form.get('country').upper()
        
        try:
            # Create a Weather object
            weather = Weather(city, state, country)
            
            # Get the latitude and longitude
            lat_lon = weather.get_lat_lon()

            if lat_lon:
                lat, lon = lat_lon
                # Fetch weather data
                weather_data = weather.get_weather(lat, lon)
                
                if weather_data:
                    # Pass weather data to the template
                    return render_template('form.html', weather_data=weather_data, city=city, state=state, country=country)
                else:
                    # Handle if weather data is not found
                    return render_template('form.html', error="Weather data not found.")
            else:
                # Handle if location is not found
                return render_template('form.html', error="Location not found.")
        except ValueError as e:
            # Handle invalid state or country codes
            return render_template('form.html', error=str(e))
        except Exception as e:
            # Handle other errors and display them on the error page
            return render_template('form.html', error=str(e))
    
    # For GET requests, render the form without weather data
    return render_template('form.html')


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
