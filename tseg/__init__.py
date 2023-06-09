# TSEG INIT 
from flask import Flask, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from tseg.config import Config
from flask_login import login_required, current_user


db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'users.login' # redirige a login si se quiere acceder sin login
login_manager.login_message_category = 'info' # brinda estetica al msg que no esta loggeado

def create_app(config_class=Config):
	app = Flask(__name__)	
	app.config.from_object(Config)
	app.config['LOGIN_MESSAGE'] = 'Por favor, inicia sesión para acceder a esta página.' #mensaje de login_required()	
	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)


	# routes se importan acá ya que routes usa "db"
	from tseg.users.routes import users	
	from tseg.equipments.routes import equipments
	from tseg.modelos.routes import modelos
	from tseg.homologaciones.routes import homologaciones
	from tseg.historias.routes import historias
	from tseg.clients.routes import clients
	from tseg.ordenes_reparacion.routes import ordenes_reparacion
	from tseg.reportes.routes import reportes
	from tseg.errors.handlers import errors	

	from tseg.users.forms import SearchForm
	

	app.register_blueprint(users)	
	app.register_blueprint(equipments)
	app.register_blueprint(modelos)
	app.register_blueprint(homologaciones)
	app.register_blueprint(historias)
	app.register_blueprint(clients)
	app.register_blueprint(ordenes_reparacion)
	app.register_blueprint(reportes)
	app.register_blueprint(errors)

		# consejo de GPT para evitar form not found
	@app.context_processor
	def inject_form():
		# Crea una instancia del formulario que quieras utilizar
		form = SearchForm()
		# Devuelve un diccionario con la variable form
		return dict(form=form)
	
	return app