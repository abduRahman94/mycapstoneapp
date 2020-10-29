from flask_sqlalchemy import SQLAlchemy
from flask import json, jsonify

db = SQLAlchemy()

class Movie(db.Model):
    __tablename__ = 'Movie'
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    actor_id = Column
    

class Actor(db.Model):
    __tablename__ = 'Actor'
    name = Column(db.String)
    age = Column(db.Integer)
    gender = Column(db.String)



