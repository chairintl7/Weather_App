from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class CityWeatherForm(FlaskForm):
    zipcode = StringField('Zip Code')
    submit = SubmitField('Enter')
