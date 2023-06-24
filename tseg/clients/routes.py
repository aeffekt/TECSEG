from flask import render_template, request, Blueprint, flash, redirect, url_for, current_app, jsonify
from flask_login import current_user, login_required
from tseg.models import Client, Equipment, Pais, Provincia, Ciudad, Domicilio, Cond_fiscal
from tseg.clients.forms import ClientForm
from tseg.users.forms import SearchForm
from tseg import db
from tseg.users.utils import role_required, obtener_informacion_geografica


clients = Blueprint('clients', __name__)


@clients.route('/obtener-datos-geograficos')
def obtener_datos_geograficos():
	codigo_postal = request.args.get('codigo_postal')
	# Utiliza la función "obtener_informacion_geografica" que definimos anteriormente
	ciudad, provincia, pais = obtener_informacion_geografica(codigo_postal)
	# Retorna los datos en formato JSON
	return jsonify(ciudad=ciudad, provincia=provincia, pais=pais)


# pass stuff to navbar through layout (used to search)
@clients.context_processor
def layout():
	form = SearchForm()
	return dict(form=form)

@clients.route("/all_clients")
@role_required("ServicioCliente", "Admin", "Técnico")
def all_clients():
	page = request.args.get('page', 1, type=int) # num pagina de mensajes
	all_clients = Client.query.order_by(Client.client_name.asc()).paginate(page=page, per_page=current_app.config['PER_PAGE'])
	return render_template('all_clients.html', all_clients=all_clients, title='Clientes')


# ruteo de variables "client_id"
@clients.route("/client-<int:client_id>")
def client(client_id):
	client = Client.query.get_or_404(client_id)	
	return render_template("client.html", title=client.client_name,
											client=client)


@clients.route("/add_client", methods=['GET','POST'] )
@role_required("ServicioCliente", "Admin")
def add_client():
	form = ClientForm()
	if form.validate_on_submit():

		# busca el ID del pais y comienza a concatenar el domicilio		
		if form.pais.data != '':			
			pais = Pais.query.filter_by(nombre=form.pais.data).first()			
		if form.provincia.data:
			provincia = Provincia.query.filter_by(nombre=form.provincia.data, pais_id=pais.id).first()
		if form.ciudad.data:
			ciudad = Ciudad.query.filter_by(nombre=form.ciudad.data, provincia_id=provincia.id).first()
		if form.domicilio.data:
			domicilio = Domicilio(direccion=form.domicilio.data, ciudad_id=ciudad.id)
			db.session.add(domicilio)					
		
		cond_fiscal = Cond_fiscal.query.filter_by(nombre=form.cond_fiscal.data).first()
		client = Client(client_name=form.client_name.data,
						business_name=form.business_name.data,
						cond_fiscal_id=cond_fiscal.id,
						cuit=form.cuit.data,
						contact=form.contact.data,
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
		if form.ciudad.data:
			ciudad = Ciudad.query.filter_by(nombre=form.ciudad.data, provincia_id=provincia.id).first()		
						
		domicilio = Domicilio.query.filter(Domicilio.id==client.domicilio.id).first()		
		domicilio.direccion = form.domicilio.data
		domicilio.ciudad_id = ciudad.id
		
		cond_fiscal = Cond_fiscal.query.filter_by(nombre=form.cond_fiscal.data).first()
		client.cond_fiscal_id = cond_fiscal.id
		client.domicilio_id = domicilio.id
		client.client_name = form.client_name.data
		client.business_name = form.business_name.data		
		client.cuit = form.cuit.data
		client.contact = form.contact.data
		client.comments = form.comments.data
		db.session.commit()
		flash("Los datos del cliente han sido actualizado", 'success')
		return redirect(url_for('clients.client', client_id=client.id))
	elif request.method == 'GET':
		form.cond_fiscal.default = client.condicion_fiscal.nombre		
		form.process()
		form.client_name.data = client.client_name
		form.business_name.data = client.business_name
		form.cuit.data = client.cuit
		form.contact.data = client.contact
		form.comments.data = client.comments

		# carga datos de domicilio si existen
		if client.domicilio:
			form.domicilio.data = client.domicilio.direccion
			if client.domicilio.ciudad:
				form.ciudad.data = client.domicilio.ciudad.nombre
				form.codigo_postal.data = client.domicilio.ciudad.cp
				if client.domicilio.ciudad.provincia:				
					form.provincia.data = client.domicilio.ciudad.provincia.nombre
					if client.domicilio.ciudad.provincia.pais:
						form.pais.data = client.domicilio.ciudad.provincia.pais.nombre
		
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
	page = request.args.get('page', 1, type=int) 
	client = Client.query.filter_by(id=client_id).first_or_404()
	equipments = Equipment.query.filter_by(owner=client)\
					.order_by(Equipment.date_modified.desc())\
					.paginate(page=page, per_page=5)
	return render_template('client_equipments.html', title=client.client_name, equipments=equipments, client=client)
