import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initializing db and loginmnager
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__) # creating a flask instance

    app.secret_key = 'why_its_dark' # creating a secret key

    basedir = os.path.abspath(os.path.dirname(__file__)) # getting the file directory of the code

    # Telling the flask-sqlalchemy to place the db inside the url of the app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')

    db.init_app(app) # adding the db inside the app

    from app import models  # Import models from the current directory
    from app.models import User

    with app.app_context(): # creating all the database tables
        db.create_all()

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except Exception as e:
            return None

    login_manager.login_view = 'login'

    from app.routes import setup_routes
    setup_routes(app)

    return app

    


    



