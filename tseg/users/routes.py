#users routes
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from tseg import db, bcrypt
from tseg.models import User, Post, Equipment, Client, Role
from tseg.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
							RequestResetForm, ResetPasswordForm, SearchForm)
from tseg.users.utils import save_picture, send_reset_email
from sqlalchemy import or_


users = Blueprint('users', __name__)


# pass stuff to navbar through layout (used to search)
@users.context_processor
def layout():
	form = SearchForm()
	return dict(form=form)

@users.route("/")
@users.route("/home")
def main():
	return render_template('main.html', title="home")


@users.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('users.main'))
	form = RegistrationForm()
	# CARGA EL VALOR 'DEFAULT' EN SELECT	
	if form.validate_on_submit():
		# creación de usuario válido y protección de contraseña
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password, role=form.role.data)
		db.session.add(user)
		db.session.commit()
		flash(f'Cuenta creada: {form.username.data}', 'success')
		login_user(user)
		return redirect(url_for("users.main"))
	elif request.method == 'GET':
		form.role.choices = Role.query.all()
		# el 1er usuario lo crea un "Admin", los demas "User" por defecto
		if User.query.first:
			form.role.default = db.session.query(Role.role_name).offset(1).limit(1).scalar()		
		else:
			form.role.default = Role.query.first()
		form.process()
	return render_template('register.html', title='Register', form=form)	


@users.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('users.main'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		# checkea en simultaneo si existe el ususario y su contraseña
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			# LOGIN: user + remember?
			login_user(user, remember=form.remember.data)
			# lleva a la pagina que se queria acceder antes de login
			next_page = request.args.get('next') # metodo request lee ruta barra direcciones
			flash(f'Sesión iniciada correctamente. Bienvenido {form.username.data}', 'success')
			return redirect(next_page) if next_page else redirect(url_for('users.main'))
		else:
			flash(f'Inicio de sesión incorrecto: {form.username.data}', 'danger')
	return render_template('login.html', title='login', form=form)	


@users.route("/logout")
def logout():
	logout_user()
	return redirect('login')


@users.route("/account", methods=['GET', 'POST'])
@login_required 
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():		
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		current_user.role = form.role.data
		db.session.commit()
		flash("La cuenta ha sido actualizada.", 'success')
		return redirect(url_for('users.account'))
	elif request.method == 'GET':
		form.role.choices = Role.query.all()
		form.role.default = current_user.role
		form.process()
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for("static", filename='profile_pics/'+current_user.image_file)
	return render_template('account.html', 
						title='Datos de cuenta', image_file=image_file, form=form)


@users.route("/user-<string:username>")
def user_posts(username):
	page = request.args.get('page', 1, type=int) #num pagina de mensajes
	user = User.query.filter_by(username=username)\
					.first_or_404()
	posts = Post.query.filter_by(author=user)\
					.order_by(Post.date_posted.desc())\
					.paginate(page=page, per_page=5)
	return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('users.main'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Un email ha sido enviado con las instrucciones para resetear su contraseña.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password-<token>", methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('users.main'))
	user = User.verify_reset_token(token)
	if user is None:
		flash('Token inválido o ha expirado', 'warning')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash(f'Su contraseña se ha cambiado con éxito!', 'success')
		login_user(user)
		return redirect(url_for("users.login"))
	return render_template('reset_token.html', title='Reset Password', form=form)


@users.route("/search", methods=['POST'])
def search():
	form = SearchForm()
	equipments = Equipment.query
	clients = Client.query
	posts = Post.query
	if form.validate_on_submit():
		searched = form.searched.data
		equipments = equipments.filter(or_(Equipment.title.like('%'+searched+'%'), \
											Equipment.content.like('%'+searched+'%'),
											Equipment.date_created.like('%'+searched+'%')
											))
		clients = clients.filter(or_(Client.client_name.like('%'+searched+'%'), \
									Client.business_name.like('%'+searched+'%'),
									Client.comments.like('%'+searched+'%'),
									Client.contact.like('%'+searched+'%'),
												))
		posts = posts.filter(Post.content.like('%'+searched+'%'))
	return render_template('search.html', title="Busqueda", 									
									searched = searched,									
									equipments=equipments,
									clients=clients,
									posts=posts)


@users.route("/users", methods=['GET', 'POST'])
def all_users():	
	page = request.args.get('page', 1, type=int) # num pagina de mensajes
	all_users = User.query.order_by(User.username.desc()).paginate(page=page, per_page=20)
	image_path = url_for("static", filename='profile_pics/')
	return render_template('all_users.html',
							all_users=all_users,
							title='Usuarios', image_path=image_path)