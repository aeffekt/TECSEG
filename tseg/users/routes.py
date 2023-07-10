#users routes
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, current_app
from flask_login import login_user, current_user, logout_user, login_required
from tseg import db, bcrypt
from tseg.models import User, Historia, Equipment, Client, Role, Marca, Modelo, Orden_reparacion
from tseg.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
							RequestResetForm, ResetPasswordForm, SearchForm)
from tseg.users.utils import save_picture, send_reset_email, role_required, buscarLista, identificador_en_corchete
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError


users = Blueprint('users', __name__)

@users.route("/")
def index():
	return render_template('index.html', title="TECSEG")


@users.route("/register", methods=['GET', 'POST'])
@role_required("Admin")
def register():	
	form = RegistrationForm()		
	if form.validate_on_submit():
		# creación de usuario válido y protección de contraseña
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		role = Role.query.filter_by(role_name=form.role.data).first()
		user = User(username=form.username.data, 
			email=form.email.data, 
			password=hashed_password, 
			role=role)
		db.session.add(user)
		db.session.commit()
		flash(f'Cuenta creada: {form.username.data}', 'success')		
		return redirect(url_for("users.all_users"))	
	return render_template('register.html', title='Registrar', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('users.index'))
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
			return redirect(next_page) if next_page else redirect(url_for('users.index'))		
		else:
			flash(f'Inicio de sesión incorrecto: {form.username.data}', 'danger')
	return render_template('login.html', title='login', form=form)	


@users.route("/logout")
def logout():
	logout_user()
	return redirect('login')


@users.route("/account-<int:user_id>", methods=['GET', 'POST'])
@login_required
def account(user_id):
	user = User.query.get_or_404(user_id)
	form = UpdateAccountForm()
	if form.validate_on_submit():		
		try:
			if form.picture.data:
				picture_file = save_picture(form.picture.data, 'profile_pics')
				user.image_file = picture_file
			user.username = form.username.data
			user.email = form.email.data
			role = Role.query.filter_by(role_name=form.role.data).first()
			user.role = role
			db.session.commit()
			flash(f"La cuenta {user.username} ha sido actualizada.", 'success')
			return redirect(url_for('users.account', user_id=user.id))
		# except especial que requiere el rollback para evitar error de ejecucion por integrityError
		except IntegrityError as err:
			db.session.rollback()
			flash(f'Ocurrió un error al intentar guardar los datos. Error: {err}', 'danger')
			return redirect(url_for('users.account', user_id=user.id))
	elif request.method == 'GET':		
		form.role.default = user.role
		form.process()
		form.username.data = user.username
		form.email.data = user.email		
	image_file = url_for("static", filename='profile_pics/'+user.image_file)
	return render_template('account.html',
						title='Datos de cuenta', image_file=image_file, form=form, user=user)


@users.route("/account-<int:user_id>", methods=['GET', 'POST'])
@role_required('Admin')
def delete_account(user_id):
	pass


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('users.index'))
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
		return redirect(url_for('users.index'))
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


@users.route("/search", methods=['GET', 'POST'])
def search():
	form = SearchForm()	
	if form.validate_on_submit():
		searched = form.searched.data
		equipments = Equipment.query.filter(or_(
												Equipment.content.like('%'+searched+'%'),
												Equipment.anio.like('%'+searched+'%'),												
												Equipment.modelo.has(
													Modelo.nombre.like('%'+searched+'%'),													
													),
												)												
											)
		
		clients = Client.query.filter(or_(Client.nombre.like('%'+searched+'%'), \
									Client.apellido.like('%'+searched+'%'),
									Client.business_name.like('%'+searched+'%'),
									Client.comments.like('%'+searched+'%'),
									Client.telefono.like('%'+searched+'%'),
									Client.email.like('%'+searched+'%'),
												))
		historias = Historia.query.filter(or_(Historia.title.like('%'+searched+'%'),
								Historia.content.like('%'+searched+'%')))
		return render_template('search.html', title="Busqueda",
									searched = searched,							
									equipments=equipments,
									clients=clients,
									historias=historias)
	if request.method == 'GET':
		return render_template('search.html')
	else:
		flash('No hay resultados, intente buscar una palabra', 'info')
		# retorna a la página que estaba, mostrando el mensaje por búqueda vacía
		return redirect(request.referrer)


@users.route("/users", methods=['GET', 'POST'])
@role_required("Admin")
def all_users():
	select_item = request.args.get('selectItem', '')
	if select_item:
		repr_split_list = select_item.split()
		# divide el __repr__ y obtiene el código en pos 2		
		user = User.query.filter_by(username=repr_split_list[0]).first()
		return redirect(url_for('users.account', user_id=user.id))
	all_users = buscarLista(User)
	image_path = url_for("static", filename='profile_pics/')
	orderBy = current_app.config["ORDER_USUARIOS"]
	item_type = 'Usuario'
	return render_template('all_users.html',
							lista=all_users,
							orderBy=orderBy,
							title='Usuarios', 
							image_path=image_path,
							item_type=item_type)


@users.route("/user-<string:username>-historias")
def user_historias(username):
	select_item = request.args.get('selectItem', '')	
	if select_item:
		historia_id = identificador_en_corchete(select_item)
		return redirect(url_for('historias.historia', historia_id=historia_id))
	user = User.query.filter_by(username=username)\
					.first_or_404()
	historias = Historia.query.filter_by(author_historia=user)\
					.order_by(Historia.date_modified.desc())
	orderBy = current_app.config["ORDER_HISTORIAS"]
	return render_template('user_historias.html', 
		orderBy=orderBy, 
		lista=historias, 
		user=user)


@users.route("/user_ordenes_reparacion-<string:user_id>")
def user_ordenes_reparacion(user_id):
	user = User.query.filter_by(id=user_id).first_or_404()
	ordenes_reparacion = Orden_reparacion.query.filter_by(author_or=user)\
					.order_by(Orden_reparacion.date_modified.desc())
	return render_template('user_ordenes_reparacion.html', title=user.user_name, ordenes_reparacion=ordenes_reparacion, user=user)