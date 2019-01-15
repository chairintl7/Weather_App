from flask import Flask, render_template
import json
import requests
app = Flask(__name__)

@app.route('/')
def index():
    url = 'http://api.openweathermap.org/data/2.5/weather?zip=95987,us&units=imperial&appid=1f55a181c9357b6ef3f0b18d331de757'    
    req = requests.get(url)
    jsonReq = req.json()
    
    city = {}
    city['name'] = jsonReq['name']
    city['country'] = jsonReq['sys']['country']
    city['temp'] = jsonReq['main']['temp']

    return render_template('index.html', title='Home', city=city)
