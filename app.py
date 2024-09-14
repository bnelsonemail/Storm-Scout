from flask import Flask, render_template, request, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from config import DevelopmentConfig  # Use DevelopmentConfig, TestingConfig or ProductionConfig
from dotenv import load_dotenv, find_dotenv
import os

# Load environment variables from the .env file
load_dotenv(find_dotenv())

app = Flask(__name__)

# Call config files
app.config.from_object(DevelopmentConfig) # Use DevelopmentConfig, TestingConfig or ProductionConfig
from dotenv import load_dotenv, find_dotenv
debug = DebugToolbarExtension(app)



# ********************  ROUTING *******************************************

@app.route('/')
def home():
    """Renders the home page with the currency conversion form."""
    return render_template('home.html')

