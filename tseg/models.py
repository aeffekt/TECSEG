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
	role = db.Column(db.String(30), unique=False, nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True) #lazy permite busqueda por esa relacion
	clients = db.relationship('Client', backref='author_cl', lazy=True)
	equipments = db.relationship('Equipment', backref='author_eq', lazy=True)
	
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

	def __repr__(self):
		return f'{self.role_name}'


class Client(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	client_name = db.Column(db.String(150), unique=False, nullable=False)
	business_name = db.Column(db.String(150), unique=False, nullable=False)
	contact = db.Column(db.String(250), unique=False, nullable=False)
	comments = db.Column(db.Text)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	equipments = db.relationship('Equipment', backref='owner', lazy=True)

	def __repr__(self):
		return f"{self.client_name}, {self.business_name}"


class Equipment(db.Model):
	now = datetime.now()
	now = now.strftime("%Y-%m-%dT%H:%M:%S")
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(150), unique=False, nullable=False)
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.fromisoformat(now))
	last_modified = db.Column(db.DateTime, nullable=False, default=datetime.fromisoformat(now))
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=True)
	
	def __repr__(self):
		return f"Equipo('{self.title}', '{self.content}')"


class Equip_data(db.Model):
	now = datetime.now()
	now = now.strftime("%Y-%m-%dT%H:%M:%S")
	id = db.Column(db.Integer, primary_key=True)
	manual_path = db.Column(db.String(150), unique=False, nullable=False)
	content = db.Column(db.Text, nullable=False)
	last_date_mod = db.Column(db.DateTime, nullable=False, default=datetime.fromisoformat(now))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Info Técnica('{self.content}', '{self.last_date_mod}')"

class Post(db.Model):
	now = datetime.now()
	now = now.strftime("%Y-%m-%dT%H:%M:%S")
	id = db.Column(db.Integer, primary_key=True)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.fromisoformat(now))
	content = db.Column(db.Text, nullable=False)
	parent_name = db.Column(db.String(150))
	parent_id = db.Column(db.Integer)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.content}', '{self.date_posted}')"