from flask import render_template, request, Blueprint, flash, redirect, url_for, current_app
from flask_login import current_user, login_required
from tseg.models import Client, Equipment, Pais, Provincia, Ciudad, Domicilio
from tseg.clients.forms import ClientForm
from tseg.users.forms import SearchForm
from tseg import db
from tseg.users.utils import role_required

clients = Blueprint('clients', __name__)

# pass stuff to navbar through layout (used to search)
@clients.context_processor
def layout():
	form = SearchForm()
	return dict(form=form)

@clients.route("/all_clients")
@role_required("ServicioCliente", "Admin", "Técnico")
def all_clients():
	page = request.args.get('page', 1, type=int) # num pagina de mensajes
	all_clients = Client.query.order_by(Client.client_name.desc()).paginate(page=page, per_page=current_app.config['PER_PAGE'])
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
		pais = Pais.query.filter_by(nombre=form.pais.data).first()		
		provincia = Provincia(nombre=form.provincia.data,
					pais_id=pais)
		db.session.add(provincia)
		db.session.commit()
		ciudad = Ciudad(cp=form.codigo_postal.data, 
						nombre=form.ciudad.data,
						provincia_id=provincia.id)
		db.session.add(ciudad)
		db.session.commit()
		domicilio = Domicilio(direccion=form.direccion.data,
								ciudad_id=ciudad.id)
		db.session.add(domicilio)
		db.session.commit()
		client = Client(client_name=form.client_name.data,
						business_name=form.business_name.data,
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
		client.client_name = form.client_name.data
		client.business_name = form.business_name.data
		client.contact = form.contact.data
		client.comments = form.comments.data
		db.session.commit()
		flash("El cliente ha sido editado con éxito", 'success')
		return redirect(url_for('clients.client', client_id=client.id))
	elif request.method == 'GET':
		form.client_name.data = client.client_name
		form.business_name.data = client.business_name
		form.contact.data = client.contact
		form.comments.data = client.comments
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
