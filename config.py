from os import environ
import redis

class Config:
	# General Config
	SECRET_KEY = environ.get('SECRET_KEY')
	FLASK_APP = environ.get('FLASK_APP')
	FLASK_ENV = environ.get('FLASK_ENV')

	# # Flask-Session
	# SESSION_TYPE = environ.get('SESSION_TYPE')
	# SESSION_REDIS = redis.from_url(environ.get('SESSION_REDIS'))

	# Flask-SQLAlchemy
	SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
	SQLALCHEMY_TRACK_MODIFICATIONS = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')