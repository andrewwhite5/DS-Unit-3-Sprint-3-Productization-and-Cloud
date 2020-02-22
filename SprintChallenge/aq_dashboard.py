"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import openaq


'''Part 2'''
APP = Flask(__name__)

api = openaq.OpenAQ()
status, body = api.measurements(city='Los Angeles', parameter='pm25')

def utc_values():
    new_list = []
    for n in range(0,100):
        my_tuple = (body['results'][n]['date']['utc'], body['results'][n]['value'])
        new_list.append(my_tuple)
    return new_list

@APP.route('/')
def root():
    return str(utc_values())


'''Part 3'''
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return Record.datetime, Record.value


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    DB.session.add(root())
    DB.session.commit()
    return 'Data refreshed!'
