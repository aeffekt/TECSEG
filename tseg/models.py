# TSEG DB MODELS
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from tseg import db, login_manager
from flask_login import UserMixin


# dar formato a la fecha actual NOW
def dateFormat():
	now = datetime.now()
	now = now.strftime("%Y-%m-%dT%H:%M:%S")
	return datetime.fromisoformat(now)


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


# tabla many to many de equipos con frecuencias de canales
equipos_frecuencias = db.Table('equipos_frecuencias',
						db.Column('equipment_id', db.Integer, db.ForeignKey('equipment.id'), primary_key=True),
						db.Column('frecuencia_id', db.Integer, db.ForeignKey('frecuencia.id'), primary_key=True))	


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
	detalles_reparacion = db.relationship('Detalle_reparacion', backref='author_detalle_reparacion', lazy=True, foreign_keys='Detalle_reparacion.user_id')
	ordenes_trabajo = db.relationship('Orden_trabajo', backref='author_ot', lazy=True, foreign_keys='Orden_trabajo.user_id')
	detalles_trabajo = db.relationship('Detalle_trabajo', backref='author_detalle_trabajo', lazy=True, foreign_keys='Detalle_trabajo.user_id')
	historias = db.relationship('Historia', backref='author_historia', lazy=True)	
	ordenes_asignadas = db.relationship('Orden_reparacion', backref='tecnicoAsignado', lazy=True, foreign_keys='Orden_reparacion.tecnico_id')
	logged_errors = db.relationship('ErrorLog', backref='user', lazy=True)

	
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
		return f"{self.username} ({self.role.role_name})"


class Role(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	role_name = db.Column(db.String(30), unique=True, nullable=False)
	user = db.relationship('User', backref='role', lazy=True)

	def __repr__(self):
		return self.role_name


class Client(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(50), unique=False, nullable=False)
	apellido = db.Column(db.String(50), unique=False, nullable=False)
	business_name = db.Column(db.String(150), unique=False, nullable=False)
	cuit = db.Column(db.String(13), unique=False, nullable=True)
	telefono = db.Column(db.String(50), unique=False, nullable=True)
	email = db.Column(db.String(150), unique=False, nullable=True)
	comments = db.Column(db.Text)	
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	domicilio_id = db.Column(db.Integer, db.ForeignKey('domicilio.id'), nullable=True)
	cond_fiscal_id = db.Column(db.Integer, db.ForeignKey('cond_fiscal.id'), nullable=True)
	iibb_id = db.Column(db.Integer, db.ForeignKey('iibb.jurisdiccion'), nullable=True)
	ordenes_trabajo = db.relationship('Orden_trabajo', backref='client', lazy=True)

	def __repr__(self):
		return f"[{self.id}] {self.nombre} {self.apellido}, {self.business_name}"


class Cond_fiscal(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(50), unique=True, nullable=False)
	clientes = db.relationship('Client', backref='cond_fiscal', lazy=True)


class Equipment(db.Model):	
	id = db.Column(db.Integer, primary_key=True)	
	numSerie = db.Column(db.String(20), nullable=True)
	anio = db.Column(db.String(4), unique=False, nullable=True)
	date_created = db.Column(db.DateTime, nullable=False, default=dateFormat())
	date_modified = db.Column(db.DateTime, nullable=False, default=dateFormat())
	content = db.Column(db.String(1000), nullable=False)	
	etiqueta_file = db.Column(db.String(50), nullable=True, default=None)
	caratula_file = db.Column(db.String(50), nullable=True, default=None)
	sistema = db.Column(db.String(25), nullable=True)	
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	detalle_trabajo_id = db.Column(db.Integer, db.ForeignKey('detalle_trabajo.id'), nullable=True)	
	modelo_id = db.Column(db.Integer, db.ForeignKey('modelo.id'), nullable=True)	
	ordenes_reparacion = db.relationship('Orden_reparacion', backref='equipo', lazy=True)
	historias = db.relationship('Historia', backref='eq_historia', lazy=True)	
	detalles_trabajo = db.relationship('Detalle_trabajo', backref='equipment', lazy=True, viewonly=True)
	frecuencias = db.relationship('Frecuencia', secondary=equipos_frecuencias, backref=db.backref('frecuencias', lazy=True))

	def __repr__(self):
		if self.numSerie:
			return f'[{self.detalle_trabajo.orden_trabajo.codigo}-{self.numSerie}] {self.modelo} ({self.detalle_trabajo.orden_trabajo.client.nombre} {self.detalle_trabajo.orden_trabajo.client.apellido})'
		else:
			return f'[{self.detalle_trabajo.orden_trabajo.codigo}] {self.modelo} ({self.detalle_trabajo.orden_trabajo.client.nombre} {self.detalle_trabajo.orden_trabajo.client.apellido})'


class Marca(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(50), unique=True, nullable=False)
	modelos = db.relationship('Modelo', backref='marca', lazy=True)

	def __repr__(self):
		return self.nombre
	

class Modelo(db.Model):	
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(50), unique=True, nullable=False)
	anio = db.Column(db.String(4), unique=False, nullable=False)
	descripcion = db.Column(db.String(250), unique=True, nullable=False)
	date_created = db.Column(db.DateTime, nullable=False, default=dateFormat())
	date_modified = db.Column(db.DateTime, nullable=False, default=dateFormat())	
	image_file = db.Column(db.String(50), nullable=False, default='default_eq.png')
	marca_id = db.Column(db.Integer, db.ForeignKey('marca.id'), nullable=True)
	homologacion_id = db.Column(db.Integer, db.ForeignKey('homologacion.id'), nullable=False)
	tipo_modelo_id = db.Column(db.Integer, db.ForeignKey('tipo_modelo.id'), nullable=False)
	equipos = db.relationship('Equipment', backref='modelo', lazy=True)

	def __repr__(self):
		if self.anio != None:
			return f'{self.nombre} {self.anio}'
		else:
			return f'{self.nombre}'


class TipoModelo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	tipo = db.Column(db.String(50), unique=True, nullable=False)
	modelos = db.relationship('Modelo', backref='tipo_modelo', lazy=True)

	def __repr__(self):
		return f'[{self.id}] {self.tipo}'
	

class Homologacion(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	codigo = db.Column(db.String(15), unique=True, nullable=False)
	modelo = db.Column(db.String(15), unique=True, nullable=False)
	modelos = db.relationship('Modelo', backref='homologacion', lazy=True)

	def __repr__(self):
		return self.codigo
	

class Frecuencia(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	canal = db.Column(db.String(50), unique=True, nullable=False)
	unidad_id = db.Column(db.Integer, db.ForeignKey('unidad.id'), nullable=False)	

	def __repr__(self):
		return f'{self.canal} {self.rango}'


class Unidad(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(10), unique=True, nullable=False)	
	frecuencias = db.relationship('Frecuencia', backref='rango', lazy=True)

	def __repr__(self):
		return self.nombre


class Historia(db.Model):	
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(150), unique=False, nullable=False)	
	date_created = db.Column(db.DateTime, nullable=False, default=dateFormat())
	date_modified = db.Column(db.DateTime, nullable=False, default=dateFormat())
	content = db.Column(db.String(1000), nullable=False)
	tipo_historia_id = db.Column(db.Integer, db.ForeignKey('tipo_historia.id'), nullable=False)
	equipo_id = db.Column(db.Integer, db.ForeignKey('equipment.id', onupdate='CASCADE'), nullable=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"{self.eq_historia.modelo.nombre} {self.title}"


class TipoHistoria(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	tipo = db.Column(db.String(50), unique=True, nullable=False)
	historias = db.relationship('Historia', backref='tipo_historia', lazy=True)

	def __repr__(self):
		return {self.tipo}


class Orden_reparacion(db.Model):	
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, nullable=False, default=dateFormat())
	date_modified = db.Column(db.DateTime, nullable=False, default=dateFormat())
	codigo = db.Column(db.String(6), unique=True, nullable=False)
	content = db.Column(db.Text, nullable=False)	
	tecnico_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False, nullable=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	equipo_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
	estado_id = db.Column(db.Integer, db.ForeignKey('estado_or.id'), nullable=False)
	detalles_reparacion = db.relationship('Detalle_reparacion', backref='orden_reparacion', lazy=True)
	

	def __repr__(self):
		return f"{self.codigo} '{self.estado}'"


class Detalle_reparacion(db.Model):	
	id = db.Column(db.Integer, primary_key=True)	
	date_created = db.Column(db.DateTime, nullable=False, default=dateFormat())
	date_modified = db.Column(db.DateTime, nullable=False, default=dateFormat())
	content = db.Column(db.Text, nullable=False)	
	reparacion_id = db.Column(db.Integer, db.ForeignKey('orden_reparacion.id', onupdate='CASCADE'), nullable=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"{self.orden_reparacion.codigo} {self.content[0:35]}"


class Estado_or(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	descripcion = db.Column(db.String(30), unique=True, nullable=False)		
	estados = db.relationship('Orden_reparacion', backref='estado', lazy=True)

	def __repr__(self):
		return self.descripcion


class Orden_trabajo(db.Model):	
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, nullable=False, default=dateFormat())
	date_modified = db.Column(db.DateTime, nullable=False, default=dateFormat())
	codigo = db.Column(db.String(6), unique=True, nullable=False)
	content = db.Column(db.String(1000), nullable=False)
	notes = db.Column(db.Text, nullable=True)
	client_id = db.Column(db.Integer, db.ForeignKey('client.id'), unique=False, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)	
	estado_id = db.Column(db.Integer, db.ForeignKey('estado_ot.id'), nullable=False)
	detalles_trabajo = db.relationship('Detalle_trabajo', backref='orden_trabajo', lazy=True)
	

	def __repr__(self):
		return f"{self.codigo} '{self.estado}'"


class Detalle_trabajo(db.Model):	
	id = db.Column(db.Integer, primary_key=True)	
	date_created = db.Column(db.DateTime, nullable=False, default=dateFormat())
	date_modified = db.Column(db.DateTime, nullable=False, default=dateFormat())
	content = db.Column(db.Text, nullable=False)
	cantidad = db.Column(db.Integer, nullable=False, default=1)
	trabajo_id = db.Column(db.Integer, db.ForeignKey('orden_trabajo.id', onupdate='CASCADE'), nullable=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	equipments = db.relationship('Equipment', backref='detalle_trabajo', lazy=True, viewonly=True)

	def __repr__(self):
		return f"{self.orden_trabajo.codigo} {self.content[0:35]}"


class Estado_ot(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	descripcion = db.Column(db.String(30), unique=True, nullable=False)		
	estados = db.relationship('Orden_trabajo', backref='estado', lazy=True)

	def __repr__(self):
		return self.descripcion


class Procedimiento(db.Model):	
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(150), unique=False, nullable=False)	
	date_created = db.Column(db.DateTime, nullable=False, default=dateFormat())
	date_modified = db.Column(db.DateTime, nullable=False, default=dateFormat())
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	user_edit_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	user = db.relationship('User', foreign_keys=[user_id], backref='author_procedimiento')
	user_edit = db.relationship('User', foreign_keys=[user_edit_id], backref='ultimo_editor')


	def __repr__(self):
		return self.title


class Domicilio(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	direccion = db.Column(db.String(150), nullable=False)	
	localidad_id = db.Column(db.Integer, db.ForeignKey('localidad.id'), nullable=True)
	clientes = db.relationship('Client', backref='domicilio', lazy=True)

	def __repr__(self):
		return f'{self.direccion}'


class Localidad(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	cp = db.Column(db.Integer, nullable=False)
	nombre = db.Column(db.String(50), nullable=False)	
	provincia_id = db.Column(db.Integer, db.ForeignKey('provincia.id'), nullable=False)
	domicilios = db.relationship('Domicilio', backref='localidad', lazy=True)

	def __repr__(self):
		return f"{self.nombre}"


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


class Iibb(db.Model):
	jurisdiccion = db.Column(db.Integer, primary_key=True)
	provincia_id = db.Column(db.Integer, db.ForeignKey('provincia.id'), nullable=True)
	provincia = db.relationship('Provincia', foreign_keys=[provincia_id], backref='provincia')
	clientes = db.relationship('Client', backref='iibb', lazy=True)

	def __repr__(self):
		return f'{self.jurisdiccion} - {self.provincia}'


class ErrorLog(db.Model):	
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, nullable=False, default=dateFormat())
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	error = db.Column(db.Text, nullable=False)	
	traceback = db.Column(db.Text, nullable=True)	

	def __repr__(self):
		return self.error
	