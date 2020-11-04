from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
database_name = "test.db"

def setupDb(app, database_name=database_name):
  app.config['SQLALCHEMY_DATABASE_URI'] = database_path = "sqlite:///{}".format(database_name)
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  db.app = app
  migrate = Migrate(app, db)
  db.init_app(app)


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




