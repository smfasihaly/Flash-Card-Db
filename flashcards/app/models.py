from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Word(db.Model):
    __tablename__ = 'words'
    id = db.Column(db.Integer, primary_key=True)
    italian = db.Column(db.String(100), nullable=False)
    english = db.Column(db.String(100), nullable=False)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)

class JustFlipped(db.Model):
    __tablename__ = 'just_flipped'
    id = db.Column(db.Integer, primary_key=True)
    italian = db.Column(db.String(100), nullable=False)
    english = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('just_flipped', lazy=True))
    language_direction = db.Column(db.String(100), nullable=False)

class Failure(db.Model):
    __tablename__ = 'failures'
    id = db.Column(db.Integer, primary_key=True)
    italian = db.Column(db.String(100))
    english = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user = db.relationship('User', backref=db.backref('failures', lazy=True))
    language_direction = db.Column(db.String(100), nullable=True)
