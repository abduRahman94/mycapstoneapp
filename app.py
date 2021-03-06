import os
from flask import (
  Flask,
  request,
  abort,
  jsonify,
  redirect,
  render_template,
  session,
  url_for
  )
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import (
  setupDb,
  db,
  Actor,
  Movie
)
from datetime import datetime
from werkzeug.exceptions import HTTPException
from six.moves.urllib.parse import urlencode
from auth import requires_auth
from auth import (
  API_AUDIENCE,
  RESPONSE_TYPE,
  CLIENT_ID,
  REDIRECT_URI,
  API_BASE_URL,
  STATE
)


database_name = 'test.db'


def create_app(test_config=None):
    app = Flask(__name__)
    setupDb(app, database_name)
    CORS(app)

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/login')
    def login():
        return redirect(API_BASE_URL +
                        '/authorize?' +
                        'audience=' +
                        API_AUDIENCE + '&' +
                        'response_type=' + RESPONSE_TYPE + '&' +
                        'client_id=' + CLIENT_ID + '&' +
                        'redirect_uri=' + REDIRECT_URI + '&' +
                        'state=' + STATE)

    @app.route('/api/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(jwt):
        actor_collection = db.session.query(Actor).all()
        actors = []

        for actor in actor_collection:
            actors.append(
                         {'name': actor.name,
                          'age': actor.age,
                          'gender': actor.gender}
                          )
        return jsonify({
                      'success': True,
                      'actors': actors
                      })

    @app.route('/api/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(jwt):
        movie_collection = db.session.query(Movie).all()
        movies = []

        for movie in movie_collection:
            if movie.actor is None:
                movies.append(
                             {'title': movie.title,
                              'date': movie.release_date,
                              'actor': ''}
                              )
            else:
                movies.append(
                             {'title': movie.title,
                              'date': movie.release_date,
                              'actor': movie.actor.name}
                             )
        return jsonify({
                       'success': True,
                       'actors': movies
                       })

    @app.route('/api/actors', methods=['POST'])
    @requires_auth('post:actor')
    def add_actor(jwt):
        body = request.get_json()
        name = body.get('name')
        age = int(body.get('age'))
        gender = body.get('gender')

        actor = Actor(name=name, age=age, gender=gender)
        try:
            db.session.add(actor)
            db.session.commit()

            return jsonify({
                          'success': True,
                          'id': actor.id
                          })

        except Exception:
            db.session.rollback()

    @app.route('/api/movies', methods=['POST'])
    @requires_auth('post:movie')
    def add_movie(jwt):
        body = request.get_json()
        title = body.get('title')
        date = body.get('release_date')
        dateTimeObj = datetime.strptime(date, "%m-%d-%y")
        actor_id = int(body.get('actor_id'))
        movie = Movie(title=title, release_date=dateTimeObj, actor_id=actor_id)

        try:
            db.session.add(movie)
            db.session.commit()

            return jsonify({
                          'success': True,
                          'id': movie.id
                          })

        except Exception:
            db.session.rollback()

    @app.route('/api/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def del_actor(jwt, id):
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
    def del_movie(jwt, id):
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
    def modif_actor(jwt, id):
        body = request.get_json()
        name = ""
        age = ""
        gender = ""

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
    def modif_movie(jwt, id):
        body = request.get_json()

        title = ""
        release_date = None

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

    return app


app = create_app()

if __name__ == '__main__':
    app.secret_key = os.environ.get('JWT_SECRET')
    app.run(host='127.0.0.1', port=8085, debug=True)
