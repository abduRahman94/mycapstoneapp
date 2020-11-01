import os
from flask import Flask, request, abort, jsonify, redirect, render_template, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
#from models import setupDb
from flask_migrate import Migrate
from datetime import datetime
#from os import environ as env
from werkzeug.exceptions import HTTPException
#from dotenv import load_dotenv, find_dotenv
#from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
from auth import requires_auth

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


client_id='L5ThqIhHIyXm1gVULmBxrvGux1a9Wlgt'
audience= 'castingapi'
api_base_url='https://castingapp.us.auth0.com'
response_type='token'
redirect_uri='http://localhost:8085/callback'
state = 'STATE'

class Movie(db.Model):
  __tablename__ = 'Movie'
  id = db.Column(db.Integer, primary_key = True)
  title = db.Column(db.String)
  release_date = db.Column(db.Date)
  actor_id = db.Column(db.ForeignKey('Actor.id'))


class Actor(db.Model):
  __tablename__ = 'Actor'
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String)
  age = db.Column(db.Integer)
  gender = db.Column(db.String)
  movies = db.relationship('Movie', backref='actor')
  

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/login')
def login():
    return redirect(api_base_url + '/authorize?' + 'audience=' + audience + '&' + 'response_type=' + response_type + '&' + 'client_id=' + client_id + '&' + 'redirect_uri=' + redirect_uri + '&' + 'state=' + state)  

@app.route('/api/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(payload):
  actor_collection = db.session.query(Actor).all()
  actors = []
  
  for actor in actor_collection:
    actors.append({'name': actor.name, 'age': actor.age, 'gender': actor.gender})
  
  return jsonify ({
    'success': True,
    'actors': actors
    })

@app.route('/api/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies():
  movie_collection = db.session.query(Movie).all()
  movies = []

  for movie in movie_collection:
    movies.append({'title': movie.title, 'date': movie.release_date, 'actor': movie.actor.name})
  
  return jsonify ({
    'success': True,
    'actors': movies
    })

@app.route('/api/actors', methods=['POST'])
@requires_auth('post:actor')
def add_actor():
  body = request.get_json()
  name = body.get('name')
  age = int(body.get('age'))
  gender = body.get('gender')

  actor = Actor(name=name, age=age, gender=gender)
  try:
    db.session.add(actor)
    db.session.commit()
    
    return jsonify({
      'sucess': True,
      'id': actor.id
    })

  except Exception:
    db.session.rollback()

@app.route('/api/movies', methods=['POST'])
@requires_auth('post:movie')
def add_movie():
  body = request.get_json()
  title = body.get('title')
  date = body.get('release_date')
  dateTimeObj = datetime.strptime(date, "%m-%d-%y")

  movie = Movie(title=title, release_date=dateTimeObj)
  try:
    db.session.add(movie)
    db.session.commit()
    
    return jsonify({
      'sucess': True,
      'id': movie.id
    })

  except Exception:
    db.session.rollback()


@app.route('/api/actors/<int:id>', methods=['DELETE'])
@requires_auth('delete:actor')
def del_actor(id):
  actor = db.session.query(Actor).filter_by(id=id).first()
  try:
    db.session.delete(actor)
    db.session.commit()
    return jsonify({
      'success': True,
      'id': actor.id
    })
  except Exception:
    db.session.rollback()


@app.route('/api/movies/<int:id>', methods=['DELETE'])
@requires_auth('delete:movie')
def del_movie(id):
  movie = db.session.query(Movie).filter_by(id=id).first()
  try:
    db.session.delete(movie)
    db.session.commit()
    return jsonify({
      'success': True,
      'id': movie.id
    })
  except Exception:
    db.session.rollback()


@app.route('/api/actors/<int:id>', methods=['PATCH']) 
@requires_auth('patch:actors')
def modif_actor(id):
  body = request.get_json()
  
  name= ""
  age= ""
  gender= ""

  if 'name' in body:
    name = body.get('name')

  if 'age' in body:
    age = int(body.get('age'))
  
  if 'gender' in body:
    gender = body.get('gender')

  
  try:
    actor = db.session.query(Actor).filter_by(id=id).first()
    
    actor.name = name
    actor.age = age
    actor.gender = gender
    db.session.commit()
    return jsonify({
      'success': True,
      'id': actor.id
    })
  
  except Exception:
    db.session.rollback()


@app.route('/api/movies/<int:id>', methods=['PATCH'])
@requires_auth('patch:movies') 
def modif_movie(id):
  body = request.get_json()
  
  title= ""
  release_date= ""

  if 'title' in body:
    title = body.get('title')

  if 'release_date' in body:
    date = body.get('release_date')
    release_date = datetime.strptime(date, '%m-%d-%y')
 

  try:
    movie = db.session.query(Movie).filter_by(id=id).first()
    
    movie.title = title
    movie.release_date = release_date
    db.session.commit()
    return jsonify({
      'success': True,
      'id': movie.id
    })
  
  except Exception:
    db.session.rollback()

@app.errorhandler(404)
def not_found(error):
  return jsonify({
    'success': False,
    'error': 404,
    'message': 'Resource not found'
  }), 400

@app.errorhandler(422)
def unprocessable(error):
  return jsonify({
    'success': False,
    'error': 422,
    'message': 'Unprocessable entity'
  }), 422

@app.errorhandler(500)
def unprocessable(error):
  return jsonify({
    'success': False,
    'error': 500,
    'message': 'Internal server error'
  }), 500

@app.errorhandler(400)
def unprocessable(error):
  return jsonify({
    'success': False,
    'error': 400,
    'message': 'Bad request'
  }), 400

#app = create_app()
if __name__ == '__main__':
  app.secret_key = 'YOUR_CLIENT_SECRET'
  app.run(host='127.0.0.1', port=8085, debug=True)
