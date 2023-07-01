from flask import render_template, request, Blueprint, flash, redirect, url_for, current_app, jsonify
from flask_login import current_user, login_required
from tseg.models import Client, Equipment, Pais, Provincia, Localidad, Domicilio, Cond_fiscal
from tseg.clients.forms import ClientForm
from tseg.users.forms import SearchForm
from tseg import db
from tseg.users.utils import role_required, obtener_informacion_geografica, buscarLista


clients = Blueprint('clients', __name__)


@clients.route('/obtener-datos-geograficos')
def obtener_datos_geograficos():
	codigo_postal = request.args.get('codigo_postal')
	# Utiliza la función "obtener_informacion_geografica" que definimos anteriormente
	localidad, provincia, pais = obtener_informacion_geografica(codigo_postal)
	# Retorna los datos en formato JSON
	return jsonify(localidad=localidad, provincia=provincia, pais=pais)


# pass stuff to navbar through layout (used to search)
@clients.context_processor
def layout():
	form = SearchForm()
	return dict(form=form)

@clients.route("/all_clients")
@role_required("ServicioCliente", "Admin", "Técnico")
def all_clients():	
	all_clients = buscarLista(Client)
	filtrar_por = current_app.config["FILTROS_CLIENTES"]				
	return render_template('all_clients.html', 
								lista=all_clients, 
								filtrar_por = filtrar_por,
								title='Clientes')


# ruteo de variables "client_id"
@clients.route("/client-<int:client_id>")
def client(client_id):
	client = Client.query.get_or_404(client_id)	
	return render_template("client.html", title=f'{client.nombre} {client.apellido}',
											client=client)


@clients.route("/add_client", methods=['GET','POST'] )
@role_required("ServicioCliente", "Admin", "Técnico")
def add_client():
	form = ClientForm()
	if form.validate_on_submit():
		# busca el ID del pais y comienza a concatenar el domicilio		
		if form.pais.data != '':			
			pais = Pais.query.filter_by(nombre=form.pais.data).first()			
		if form.provincia.data:
			provincia = Provincia.query.filter_by(nombre=form.provincia.data, pais_id=pais.id).first()
		if form.localidad.data:
			localidad = Localidad.query.filter_by(nombre=form.localidad.data, provincia_id=provincia.id).first()
		if form.domicilio.data:
			domicilio = Domicilio(direccion=form.domicilio.data, localidad_id=localidad.id)
			db.session.add(domicilio)
		
		cond_fiscal = Cond_fiscal.query.filter_by(nombre=form.cond_fiscal.data).first()
		client = Client(nombre=form.nombre.data,
						apellido=form.apellido.data,
						business_name=form.business_name.data,
						cond_fiscal_id=cond_fiscal.id,
						cuit=form.cuit.data,
						telefono=form.telefono.data,
						email=form.email.data,
						comments=form.comments.data,
						domicilio_id=domicilio.id,
						author_cl=current_user)
		db.session.add(client)
		db.session.commit()			
		flash('Cliente agregado!', 'success')
		return redirect(url_for('clients.client', client_id=client.id))
	return render_template('create_client.html', title='Nuevo cliente', 
												form=form,
												legend="Registrar cliente")

@clients.route("/client-<int:client_id>-update", methods=['GET', 'POST'])
@role_required("ServicioCliente", "Admin", "Técnico")
def update_client(client_id):
	client = Client.query.get_or_404(client_id)
	form = ClientForm()
	if form.validate_on_submit():
		if form.pais.data != '':			
			pais = Pais.query.filter_by(nombre=form.pais.data).first()			
		if form.provincia.data:
			provincia = Provincia.query.filter_by(nombre=form.provincia.data, pais_id=pais.id).first()
		if form.localidad.data:
			localidad = Localidad.query.filter_by(nombre=form.localidad.data, provincia_id=provincia.id).first()		
		domicilio = Domicilio.query.filter(Domicilio.id==client.domicilio.id).first()		
		domicilio.direccion = form.domicilio.data
		domicilio.localidad_id = localidad.id		
		cond_fiscal = Cond_fiscal.query.filter_by(nombre=form.cond_fiscal.data).first()
		client.cond_fiscal_id = cond_fiscal.id
		client.domicilio_id = domicilio.id
		client.nombre = form.nombre.data
		client.apellido = form.apellido.data
		client.business_name = form.business_name.data		
		client.cuit = form.cuit.data
		client.telefono = form.telefono.data
		client.email = form.email.data
		client.comments = form.comments.data
		db.session.commit()
		flash("Los datos del cliente han sido actualizado", 'success')
		return redirect(url_for('clients.client', client_id=client.id))
	elif request.method == 'GET':
		form.cond_fiscal.default = client.condicion_fiscal.nombre		
		form.process()
		form.nombre.data = client.nombre
		form.apellido.data = client.apellido
		form.business_name.data = client.business_name
		form.cuit.data = client.cuit
		form.telefono.data = client.telefono
		form.email.data = client.email
		form.comments.data = client.comments

		# carga datos de domicilio si existen
		if client.domicilio:
			form.domicilio.data = client.domicilio.direccion
			if client.domicilio.localidad:
				form.localidad.data = client.domicilio.localidad.nombre
				form.codigo_postal.data = client.domicilio.localidad.cp
				if client.domicilio.localidad.provincia:				
					form.provincia.data = client.domicilio.localidad.provincia.nombre
					if client.domicilio.localidad.provincia.pais:
						form.pais.data = client.domicilio.localidad.provincia.pais.nombre
		
	return render_template('create_client.html',title='Editar cliente', 
												form=form,
												legend="Editar cliente")

@clients.route("/client-<int:client_id>-delete", methods=['POST'])
@role_required("ServicioCliente", "Admin")
def delete_client(client_id):
	client = Client.query.get_or_404(client_id)
	db.session.delete(client)
	db.session.commit()
	flash("El cliente ha sido eliminado!", 'success')
	return redirect(url_for('clients.all_clients'))


@clients.route("/client_equipments-<string:client_id>")
def client_equipments(client_id):	
	client = Client.query.filter_by(id=client_id).first_or_404()
	equipments = Equipment.query.filter_by(owner=client)\
					.order_by(Equipment.date_modified.desc())	
	filtrar_por = current_app.config["FILTROS_EQUIPOS"]
	image_path = url_for("static", filename='models_pics/')
	return render_template('client_equipments.html',
								title=f'{client.nombre} {client.apellido}',
								filtrar_por=filtrar_por,
								lista=equipments,
								image_path=image_path,
								client=client)
