# imports! ---> moduli da installare nei nuovi progetti flask, flask-login, flask-sqlalchemy
from flask import Flask
import secrets
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)

    #creazione chiave segreta dell'app
    secret = secrets.token_urlsafe(32)
    app.secret_key = secret
    #database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    #registra il blueprint
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    #CONTROLLO SE IL DATABASE ESISTE GIA
    from .models import User, Note
    create_database(app)

    #avvio il login manager, definisco dove vado se non ho fatto il login con login view
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  #cerco per id ,

    #avvio app
    return app


#funzione che crea database se non esiste
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
