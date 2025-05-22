import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
	app = Flask(__name__) # creating a flask instance

	app.secret_key = 'why_its_dark' # creating a secret key

	basedir = os.path.abspath(os.path.dirname(__file__)) # getting the file directory of the code

	# telling the flask-sqlalchemy to place the db inside the url of the app
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')

	db.init_app(app) # adding the db inside the app

	from app import models  # Import models from the current directory
	
	with app.app_context(): # creating all the database tables
		db.create_all()

	# Initializing the Login manager and adding it to the code
	login_manager = LoginManager()
	login_manager.init_app(app)

	from app.routes import setup_routes
	setup_routes(app)

	return app

	


	



