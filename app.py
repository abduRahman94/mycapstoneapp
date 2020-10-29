import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

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
  
  
@app.route('/api/actors', methods=['GET'])
def get_actors():
  actor_collection = db.session.query(Actor).all()
  actors = []
  
  for actor in actor_collection:
    actors.append({'name': actor.name, 'age': actor.age, 'gender': actor.gender})
  
  return jsonify ({
    'success': True,
    'actors': actors
    })

@app.route('/api/movies', methods=['GET'])
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
    'message': 'resource not found'
  }), 400

#app = create_app()
if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8085, debug=True)
