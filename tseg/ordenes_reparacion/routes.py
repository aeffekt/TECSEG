# Orden_reparacions routes
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, current_app
from flask_login import current_user, login_required
from tseg import db
from tseg.models import Orden_reparacion, Equipment
from tseg.ordenes_reparacion.forms import OrdenReparacionForm
from tseg.users.forms import SearchForm
from tseg.users.utils import role_required, extraerId
from datetime import datetime

ordenes_reparacion = Blueprint('ordenes_reparacion', __name__)


# pass stuff to navbar through layout (used to search)
@ordenes_reparacion.context_processor
def layout():
	form = SearchForm()
	return dict(form=form)

@ordenes_reparacion.route("/all_ordenes_reparacion")
def all_ordenes_reparacion():
	page = request.args.get('page', 1, type=int) # num pagina de mensajes
	all_or = Orden_reparacion.query.order_by(Orden_reparacion.date_created.desc()).paginate(page=page, per_page=current_app.config['PER_PAGE'])
	return render_template('all_ordenes_reparacion.html', 
							all_ordenes_reparacion=all_or, 
							title='Órdenes de reparación')

# ruteo de variables "Orden_reparacion_id"
@ordenes_reparacion.route("/orden_reparacion-<int:orden_reparacion_id>")
def orden_reparacion(orden_reparacion_id):
	orden_reparacion = Orden_reparacion.query.get_or_404(orden_reparacion_id)
	return render_template("orden_reparacion.html", orden_reparacion=orden_reparacion)


@ordenes_reparacion.route("/add_orden_reparacion-<string:equipment_id>", methods=['GET','POST'] )
@role_required("Admin", "Técnico", "ServicioCliente")
def add_orden_reparacion(equipment_id):
	form = OrdenReparacionForm()	
	if form.validate_on_submit():		
		tecnico_id = extraerId(form.tecnico.data)
		equipo_id = extraerId(form.equipo.data)
		orden_reparacion = Orden_reparacion(
							codigo=form.codigo.data, 
							content=form.content.data, 													
							author_or=current_user, 
							tecnico_id=tecnico_id,
							equipment_id=equipo_id)
		db.session.add(orden_reparacion)
		db.session.commit()
		flash(f'Orden de reparación {orden_reparacion.codigo} agregada!', 'success')
		return redirect(url_for('ordenes_reparacion.orden_reparacion', orden_reparacion_id=orden_reparacion.id))
	elif request.method == 'GET':
		equipment = Equipment.query.filter_by(id=equipment_id).first()
		if(equipment): # CARGA EL VALOR 'DEFAULT' EN SELECT si encuentra un equipo
			form.equipo.default = f'[{equipment.id}] {equipment.title} ({equipment.owner.client_name})'
			form.process() 
	return render_template('create_orden_reparacion.html', title='Agregar O.R.', 
												form=form, legend="Crear órden de reparación")


@ordenes_reparacion.route("/orden_reparacion-<int:orden_reparacion_id>-update", methods=['GET', 'POST'])
@login_required
def update_orden_reparacion(orden_reparacion_id):
	orden_reparacion = Orden_reparacion.query.get_or_404(orden_reparacion_id)
	if orden_reparacion.author_or != current_user:
		abort(403) #http forbidden
	form = OrdenReparacionForm()
	if form.validate_on_submit():
		equipment_id = extraerId(form.equipo.data)
		user_id = extraerId(form.tecnico.data)
		orden_reparacion.equipo_id = equipment_id		
		orden_reparacion.tecnico_id = user_id
		now = datetime.now()
		now = now.strftime("%Y-%m-%dT%H:%M:%S")
		orden_reparacion.date_modified = datetime.fromisoformat(now)
		orden_reparacion.codigo = form.codigo.data
		orden_reparacion.content = form.content.data
		db.session.commit()
		flash("Su órden de reparacion ha sido editada con éxito", 'success')
		return redirect(url_for('ordenes_reparacion.orden_reparacion', orden_reparacion_id=orden_reparacion.id))
	elif request.method == 'GET':
		# si no hay tecnico asignado lo deja vacio
		if orden_reparacion.tecnicoAsignado:
			form.tecnico.default = f'[{orden_reparacion.tecnicoAsignado.id}] {orden_reparacion.tecnicoAsignado.username} ({orden_reparacion.tecnicoAsignado.role.role_name})'
		form.equipo.default = f'[{orden_reparacion.equipo.id}] {orden_reparacion.equipo.title} ({orden_reparacion.equipo.owner.client_name})'		
		form.process()
		form.codigo.data = orden_reparacion.codigo
		form.content.data = orden_reparacion.content	
	return render_template('create_orden_reparacion.html', 	title='Editar Orden reparacion', 
												form=form,
												legend="Editar Orden reparacion")

@ordenes_reparacion.route("/orden_reparacion-<int:orden_reparacion_id>-delete", methods=['POST'])
@role_required("Admin", "Técnico")
def delete_orden_reparacion(orden_reparacion_id):
	orden_reparacion = Orden_reparacion.query.get_or_404(orden_reparacion_id)
	if orden_reparacion.author_or != current_user:
		abort(403)
	db.session.delete(orden_reparacion)
	db.session.commit()
	flash(f"La órden de reparacion {orden_reparacion.codigo} ha sido eliminada!", 'success')
	return redirect(url_for('ordenes_reparacion.all_ordenes_reparacion'))