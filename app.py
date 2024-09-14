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
app.config.from_object(DevelopmentConfig) # Use DevelopmentConfig, TestingConfig or ProductionConfig
from dotenv import load_dotenv, find_dotenv
debug = DebugToolbarExtension(app)

w = Weather()

# ********************  ROUTING *******************************************

@app.route('/')
def home():
    """Renders the home page with the currency conversion form."""
    return render_template('home.html')


@app.route('/form')
def form():
    """Renders the page for the user to enter the data into the form"""
    return render_template('form.html')

@app.route('/results')
def results():
    """Handles form submission, calls the Weather API, and redirects to #form """
    city = request.form.get('city').lower()
    state = request.form.get('state').upper()
    country = request.form.get('country').upper()
    
    try:
        # Store the results in the session
        session[city] = city
        session[state] = state
        session[country] = country
        
        
        # Redirects to #form to display the results
        return redirect('#form')
    except ValueError as e:
        # Handle invalid state or country codes
        return render_template('home.html', error=str(e)), 400
    except Exception as e:
        # Handle other errors and display them on the error page
        return render_template('error.html', error=str(e)), 500
        



if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)