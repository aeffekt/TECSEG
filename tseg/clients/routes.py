from flask import render_template, request, Blueprint, flash, redirect, url_for, current_app, jsonify
from flask_login import current_user, login_required
from tseg.models import Client, Equipment, Pais, Provincia, Localidad, Domicilio, Cond_fiscal
from tseg.clients.forms import ClientForm
from tseg import db
from tseg.users.utils import role_required, obtener_informacion_geografica, buscarLista,identificador_en_corchete


clients = Blueprint('clients', __name__)


@clients.route('/obtener-datos-geograficos')
def obtener_datos_geograficos():
	codigo_postal = request.args.get('codigo_postal')
	# Utiliza la función "obtener_informacion_geografica" que definimos anteriormente
	localidad, provincia, pais = obtener_informacion_geografica(codigo_postal)
	# Retorna los datos en formato JSON
	return jsonify(localidad=localidad, provincia=provincia, pais=pais)

@clients.route("/all_clients")
@role_required("ServicioCliente", "Admin", "Técnico")
def all_clients():
	select_item = request.args.get('selectItem', '')
	if select_item:
		client_id = identificador_en_corchete(select_item)
		return redirect(url_for('clients.client', client_id=client_id))
		
	all_clients = buscarLista(Client)
	orderBy = current_app.config["ORDER_CLIENTES"]
	item_type = 'Cliente'
	return render_template('all_clients.html', 
								lista=all_clients, 
								orderBy = orderBy,
								title='Clientes',
								item_type=item_type)


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
		try:
			# busca el ID del pais y comienza a concatenar el domicilio		
			if form.pais.data != '':			
				pais = Pais.query.filter_by(nombre=form.pais.data).first()
				if not pais:
					pais=Pais(nombre=form.pais.data)
					db.session.add(pais)				
			if form.provincia.data:
				provincia = Provincia.query.filter_by(nombre=form.provincia.data, pais=pais).first()
				if not provincia:
					provincia=Provincia(nombre=form.provincia.data, pais=pais)
					db.session.add(provincia)				
			if form.localidad.data:
				localidad = Localidad.query.filter_by(nombre=form.localidad.data, provincia=provincia).first()
				if not localidad:
					localidad=Localidad(nombre=form.localidad.data, cp=form.codigo_postal.data, provincia=provincia)
					db.session.add(localidad)
			else:
				localidad = None
			domicilio = Domicilio.query.filter_by(direccion=form.domicilio.data)\
										.join(Domicilio.localidad)\
										.filter(Localidad.nombre == form.localidad.data).first()
			if not domicilio:			
				domicilio = Domicilio(direccion=form.domicilio.data, localidad=localidad)
				db.session.add(domicilio)		
			cond_fiscal = Cond_fiscal.query.filter_by(nombre=form.cond_fiscal.data).first()
			client = Client(nombre=form.nombre.data,
							apellido=form.apellido.data,
							business_name=form.business_name.data,
							cond_fiscal=cond_fiscal,
							cuit=form.cuit.data,
							telefono=form.telefono.data,
							email=form.email.data,
							comments=form.comments.data,
							domicilio=domicilio,
							author_cl=current_user)
		
			db.session.add(client)
			db.session.commit()		
			flash('Cliente agregado!', 'success')
			return redirect(url_for('clients.client', client_id=client.id))
		except Exception as err:
			flash(f'Ocurrió un error al intentar guardar los datos. Error: {err}', 'danger')
			return redirect(url_for('clients.add_client'))
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
		try:
			db.session.commit()
			flash("Los datos del cliente han sido actualizado", 'success')
			return redirect(url_for('clients.client', client_id=client.id))
		except Exception as err:
			flash(f'Ocurrió un error al intentar guardar los datos. Error: {err}', 'danger')
			return redirect(url_for('clients.client', client_id=client.id))
			
	elif request.method == 'GET':
		form.cond_fiscal.default = client.cond_fiscal.nombre		
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
	db.session.delete(client.domicilio)
	db.session.delete(client)
	db.session.commit()
	flash("El cliente ha sido eliminado!", 'success')
	return redirect(url_for('clients.all_clients'))


@clients.route("/client_equipments-<string:client_id>")
def client_equipments(client_id):	
	client = Client.query.filter_by(id=client_id).first_or_404()
	equipments = Equipment.query.filter_by(owner=client)\
					.order_by(Equipment.date_modified.desc())	
	orderBy = current_app.config["ORDER_EQUIPOS"]
	image_path = url_for("static", filename='models_pics/')
	return render_template('client_equipments.html',
								title=f'{client.nombre} {client.apellido}',
								orderBy=orderBy,
								lista=equipments,
								image_path=image_path,
								client=client)
