# TSEG DB MODELS
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from tseg import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

# Tablas de la base de datos en forma de clases
class User(db.Model, UserMixin):	
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), unique=True, nullable=False)
	email = db.Column(db.String(50), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(32), unique=True, nullable=False)	
	role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)	
	clients = db.relationship('Client', backref='author_cl', lazy=True)
	equipments = db.relationship('Equipment', backref='author_eq', lazy=True)
	ordenes_reparacion = db.relationship('Orden_reparacion', backref='author_or', lazy=True, foreign_keys='Orden_reparacion.user_id')
	historias = db.relationship('Historia', backref='author_historia', lazy=True)
	ordenes_asignadas = db.relationship('Orden_reparacion', backref='tecnicoAsignado', lazy=True, foreign_keys='Orden_reparacion.tecnico_id')

	
	def get_reset_token(self, expires_sec=1800):
		s= Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s= Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}')"


class Role(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	role_name = db.Column(db.String(30), unique=True, nullable=False)
	user = db.relationship('User', backref='role', lazy=True)

	def __repr__(self):
		return f'{self.role_name}'


class Client(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(50), unique=False, nullable=False)
	apellido = db.Column(db.String(50), unique=False, nullable=False)
	business_name = db.Column(db.String(150), unique=False, nullable=False)
	cuit = db.Column(db.String(13), unique=False, nullable=True)
	telefono = db.Column(db.String(20), unique=False, nullable=True)
	email = db.Column(db.String(150), unique=False, nullable=True)
	comments = db.Column(db.Text)	
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	domicilio_id = db.Column(db.Integer, db.ForeignKey('domicilio.id'), nullable=True)
	cond_fiscal_id = db.Column(db.Integer, db.ForeignKey('cond_fiscal.id'), nullable=True)
	equipments = db.relationship('Equipment', backref='owner', lazy=True)

	def __repr__(self):
		return f"{self.nombre} {self.apellido}, {self.business_name}"

class Cond_fiscal(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(50), unique=True, nullable=False)
	clientes = db.relationship('Client', backref='condicion_fiscal', lazy=True)


class Equipment(db.Model):
	now = datetime.now()
	now = now.strftime("%Y-%m-%dT%H:%M:%S")
	id = db.Column(db.Integer, primary_key=True)	
	numSerie = db.Column(db.String(20), unique=False, nullable=True)
	anio = db.Column(db.String(4), unique=False, nullable=True)	
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.fromisoformat(now))
	date_modified = db.Column(db.DateTime, nullable=False, default=datetime.fromisoformat(now))
	content = db.Column(db.Text, nullable=False)	
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=True)
	marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'), nullable=True)
	modelo_id = db.Column(db.Integer, db.ForeignKey('modelo.id'), nullable=True)
	frecuencia_id = db.Column(db.Integer, db.ForeignKey('frecuencia.id'), nullable=True)
	orden_reparacion = db.relationship('Orden_reparacion', backref='equipo', lazy=True)
	historias = db.relationship('Historia', backref='equipo_historia', lazy=True)
	
	def __repr__(self):
		return f"Equipo('{self.title}', '{self.content}')"


class Marca(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(50), unique=True, nullable=False)
	equipos = db.relationship('Equipment', backref='marca_eq', lazy=True)


class Modelo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(50), unique=True, nullable=False)
	equipos = db.relationship('Equipment', backref='modelo_eq', lazy=True)

class Frecuencia(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	canal = db.Column(db.String(50), unique=True, nullable=False)
	equipos = db.relationship('Equipment', backref='frecuencia_eq', lazy=True)


class Historia(db.Model):
	now = datetime.now()
	now = now.strftime("%Y-%m-%dT%H:%M:%S")
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(150), unique=False, nullable=False)	
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.fromisoformat(now))
	date_modified = db.Column(db.DateTime, nullable=False, default=datetime.fromisoformat(now))
	content = db.Column(db.Text, nullable=False)
	tipologia_id = db.Column(db.Integer, db.ForeignKey('tipologia.id'), nullable=False)
	equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)	

	def __repr__(self):
		return f"Historia de equipo('{self.equipment_id}', '{self.title}')"

class Tipologia(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	tipo = db.Column(db.String(50), unique=True, nullable=False)
	historias = db.relationship('Historia', backref='tipologia', lazy=True)

	def __repr__(self):
		return f'{self.estado}'

class Orden_reparacion(db.Model):
	now = datetime.now()
	now = now.strftime("%Y-%m-%dT%H:%M:%S")
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.fromisoformat(now))
	date_modified = db.Column(db.DateTime, nullable=False, default=datetime.fromisoformat(now))
	codigo = db.Column(db.String(50), unique=False, nullable=False)
	content = db.Column(db.Text, nullable=False)	
	tecnico_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False, nullable=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	equipo_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
	estado_id = db.Column(db.Integer, db.ForeignKey('estado_or.id'), nullable=False)	
	

	def __repr__(self):
		return f"{self.codigo}', '{self.fecha_modificado}'"


class Estado_or(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	descripcion = db.Column(db.String(30), unique=True, nullable=False)		
	estados = db.relationship('Orden_reparacion', backref='estado', lazy=True)

	def __repr__(self):
		return f'{self.estado}'


class Domicilio(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	direccion = db.Column(db.String(150), nullable=False)	
	localidad_id = db.Column(db.Integer, db.ForeignKey('localidad.id'), nullable=True)
	clientes = db.relationship('Client', backref='domicilio', lazy=True)

	def __repr__(self):
		return f'{self.direccion}'


class Localidad(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	cp = db.Column(db.String(15), nullable=False)
	nombre = db.Column(db.String(50), nullable=False)	
	provincia_id = db.Column(db.Integer, db.ForeignKey('provincia.id'), nullable=True)
	domicilios = db.relationship('Domicilio', backref='localidad', lazy=True)

	def __repr__(self):
		return f'{self.cp}'


class Provincia(db.Model):
	id = db.Column(db.Integer, primary_key=True)	
	nombre = db.Column(db.String(50), nullable=False)	
	pais_id = db.Column(db.Integer, db.ForeignKey('pais.id'), nullable=True)
	localidades = db.relationship('Localidad', backref='provincia', lazy=True)

	def __repr__(self):
		return f'{self.nombre}'


class Pais(db.Model):
	id = db.Column(db.Integer, primary_key=True)	
	nombre = db.Column(db.String(50), nullable=False)		
	provincias = db.relationship('Provincia', backref='pais', lazy=True)

	def __repr__(self):
		return f'{self.nombre}'