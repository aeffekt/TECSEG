from flask import render_template, request, Blueprint, flash, redirect, url_for, current_app, jsonify
from flask_login import current_user, login_required
from tseg.models import (Client, Equipment, Pais, Provincia, Localidad, 
						 Domicilio, Cond_fiscal, Iibb, Orden_trabajo, Detalle_trabajo)
from tseg.clients.forms import ClientForm
from tseg import db
from tseg.users.utils import role_required, obtener_informacion_geografica, buscarLista, error_logger


clients = Blueprint('clients', __name__)


@clients.route('/obtener-datos-geograficos')
def obtener_datos_geograficos():
	codigo_postal = request.args.get('codigo_postal')
	# Utiliza la función "obtener_informacion_geografica"
	localidad, provincia, pais = obtener_informacion_geografica(codigo_postal)
	# Retorna los datos en formato JSON
	return jsonify(localidad=localidad, provincia=provincia, pais=pais)


@clients.route("/all_clients")
@login_required
def all_clients():
	select_item = request.args.get('selectItem', '')
	if select_item:		
		return redirect(url_for('clients.client', client_id=select_item))		
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
@login_required
def client(client_id):
	client = Client.query.get_or_404(client_id)	
	ordenes_trabajo =  buscarLista(Orden_trabajo, client)	
	orderBy = current_app.config['ORDER_OT']	
	# texto para toolbar
	item_type="Órdenes de Trabajo"	
	return render_template("client.html", title=f'{client.nombre} {client.apellido}',
											client=client,											
											legend="Ver Orden de Trabajo",
											orderBy = orderBy,
											lista=ordenes_trabajo,
											item_type=item_type,	)


@clients.route("/add_client", methods=['GET','POST'] )
@role_required("ServicioCliente", "Admin", "Comercial")
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
				provincia = Provincia.query.filter_by(nombre=form.provincia.data, pais=pais).first()
				if not provincia:
					provincia=Provincia(nombre=form.provincia.data, pais=pais)
					db.session.add(provincia)			
				localidad = Localidad.query.filter_by(nombre=form.localidad.data, provincia=provincia).first()
				if not localidad:
					localidad=Localidad(nombre=form.localidad.data.upper(), cp=form.codigo_postal.data, provincia=provincia)
					db.session.add(localidad)
			else:
				localidad = None
			# busca para no repetir identico domicilio
			domicilio = Domicilio.query.filter_by(direccion=form.direccion.data)\
										.join(Domicilio.localidad)\
										.filter(Localidad.nombre == form.localidad.data).first()
			if not domicilio:			
				domicilio = Domicilio(direccion=form.direccion.data, localidad=localidad)
				db.session.add(domicilio)	
			cond_fiscal = Cond_fiscal.query.get(form.cond_fiscal.data)
			iibb = Iibb.query.get(form.iibb.data)
			client = Client(nombre=form.nombre.data,
							apellido=form.apellido.data,
							business_name=form.business_name.data,
							cond_fiscal=cond_fiscal,
							iibb=iibb,
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
		except Exception as e:
			error_logger(e)
			return redirect(url_for('clients.add_client'))
	return render_template('create_client.html', title='Nuevo cliente', 
												form=form,
												legend="Registrar cliente")


@clients.route("/client-<int:client_id>-update", methods=['GET', 'POST'])
@role_required("ServicioCliente", "Admin", "Técnico", "Comercial")
def update_client(client_id):
	client = Client.query.get_or_404(client_id)
	form = ClientForm(client)
	if form.validate_on_submit():
		try:
			domicilio = Domicilio.query.filter(Domicilio.id==client.domicilio.id).first()		
			domicilio.direccion = form.direccion.data
			if form.pais.data != '':			
					pais = Pais.query.filter_by(nombre=form.pais.data).first()
					if not pais:
						pais=Pais(nombre=form.pais.data)
						db.session.add(pais)			
					provincia = Provincia.query.filter_by(nombre=form.provincia.data, pais=pais).first()
					if not provincia:
						provincia=Provincia(nombre=form.provincia.data, pais=pais)
						db.session.add(provincia)
					localidad = Localidad.query.filter_by(nombre=form.localidad.data.upper(), provincia=provincia).first()
					if not localidad:
						localidad=Localidad(nombre=form.localidad.data, cp=form.codigo_postal.data, provincia=provincia)
						db.session.add(localidad)
					domicilio.localidad = localidad
			else:
				client.pais=None
				client.provincia=None
				client.localidad=None
				client.domicilio.direccion=''
				client.domicilio.localidad=None
			client.cond_fiscal_id = form.cond_fiscal.data			
			client.iibb_id = form.iibb.data				
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
		except Exception as e:
			error_logger(e)
			return redirect(url_for('clients.client', client_id=client.id))
			
	elif request.method == 'GET':
		if client.cond_fiscal:
			form.cond_fiscal.default = client.cond_fiscal.id		
		if client.iibb:
			form.iibb.default = client.iibb.jurisdiccion		
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
			form.direccion.data = client.domicilio.direccion
			if client.domicilio.localidad:
				form.localidad.data = client.domicilio.localidad.nombre
				form.codigo_postal.data = client.domicilio.localidad.cp
				form.provincia.data = client.domicilio.localidad.provincia.nombre
				form.pais.data = client.domicilio.localidad.provincia.pais.nombre
		
	return render_template('create_client.html',title='Editar cliente', 
												form=form,
												legend="Editar cliente")


@clients.route("/client-<int:client_id>-delete", methods=['POST'])
@role_required("ServicioCliente", "Admin")
def delete_client(client_id):
	client = Client.query.get_or_404(client_id)
	try:	
		db.session.delete(client.domicilio)
		db.session.delete(client)
		db.session.commit()
		flash("El cliente ha sido eliminado!", 'success')
		return redirect(url_for('clients.all_clients', orderBy='id', orderOrder='asc'))
	except Exception as e:
		db.session.rollback() 
		flash("Ocurrió un error al intentar eliminar.", 'danger')		
		flash(f" Es probable que existan equipos u O.T. asignados al cliente.", 'danger')		
		return redirect(url_for('clients.client', client_id=client.id))	


@clients.route("/client_equipments-<string:client_id>")
@login_required
def client_equipments(client_id):
	select_item = request.args.get('selectItem', '')	
	if select_item:		
		return redirect(url_for('equipments.equipment', equipment_id=select_item))	
	client = Client.query.filter_by(id=client_id).first_or_404()
	equipos_del_cliente  = Equipment.query.join(Detalle_trabajo)\
								.join(Orden_trabajo)\
									.filter(Orden_trabajo.client_id == client_id)\
										.order_by(Equipment.date_modified.desc())
	
	orderBy = current_app.config["ORDER_EQUIPOS"]
	image_path = url_for("static", filename='models_pics/')
	return render_template('client_equipments.html',
								title=f'{client.nombre} {client.apellido}',
								orderBy=orderBy,
								lista=equipos_del_cliente,
								image_path=image_path,
								client=client)
