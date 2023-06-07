# TSEG INIT 
from flask import Flask, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from tseg.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'users.login' # redirige a login si se quiere acceder sin login
login_manager.login_message_category = 'info' # brinda estetica al msg que no esta loggeado


def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	# routes se importan acá ya que routes usa "db"
	from tseg.users.routes import users
	from tseg.posts.routes import posts
	from tseg.equipments.routes import equipments
	from tseg.clients.routes import clients
	from tseg.errors.handlers import errors
	
	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(equipments)
	app.register_blueprint(clients)
	app.register_blueprint(errors)

	return app