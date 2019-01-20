from flask import Flask, render_template, request, url_for, redirect
from forms import CityWeatherForm
from flask_sqlalchemy import SQLAlchemy
import json
import requests
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
app.secret_key = 'development key'

#Models
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    zipcode = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(3), nullable=False)
    temperature = db.Column(db.Integer, nullable=False)
    weather = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"City({self.id, self.name, self.country, self.temperature, self.weather})"

@app.route('/', methods = ['POST', 'GET'])
def index():
    form = CityWeatherForm() 
    cities = update_cities_weather()
    
    if request.method == 'POST':
        if form.zipcode.data:
            city = get_city_weather(form.zipcode.data)
            if city != None:
                db.session.add(city)
                db.session.commit()	
        return redirect(url_for('index'))

    return render_template('index.html', form=form, cities = cities)

@app.route('/delete/<zipcode>')
def delete(zipcode):
    delete_city = City.query.filter_by(zipcode = zipcode).first()

    db.session.delete(delete_city)
    db.session.commit()
    return redirect(url_for('index'))
    
#helper methods
def update_cities_weather():
    cities = City.query.all()
    for c in cities:
        update_city = get_city_weather(c.zipcode)
        
        c.name = update_city.name
        c.country = update_city.country
        c.temperature = update_city.temperature
        c.zipcode = update_city.zipcode
        c.weather = update_city.weather

        db.session.commit()

    return City.query.all()
    
def get_city_weather(zip):
    url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid=1f55a181c9357b6ef3f0b18d331de757'.format(zip)    
    
    req = requests.get(url)
    jsonReq = req.json()

    if jsonReq['cod'] != '400' and jsonReq['cod'] != '404':
        new_city = City()
        new_city.name = jsonReq['name']
        new_city.country = jsonReq['sys']['country']
        new_city.temperature = jsonReq['main']['temp']
        new_city.zipcode = zip
        new_city.weather = jsonReq['weather'][0]['description']
    
        return new_city
    else:
        return None
