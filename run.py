from flask import Flask
import json
import requests
app = Flask(__name__)

@app.route('/')
def index():
    url = 'https://api.openweathermap.org/data/2.5/weather?q=London,uk&appid=1f55a181c9357b6ef3f0b18d331de757'    
    req = requests.get(url)

 
    name = req.json()['name']
    weather = req.json()['weather'][0]['main']
    
    return weather

    