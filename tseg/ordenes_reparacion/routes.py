# Orden_reparacions routes
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, current_app
from flask_login import current_user, login_required
from tseg import db
from tseg.models import Orden_reparacion, Equipment, Estado_or
from tseg.ordenes_reparacion.forms import OrdenReparacionForm
from tseg.users.forms import SearchForm
from tseg.users.utils import role_required, extraerId, dateFormat, buscarLista


ordenes_reparacion = Blueprint('ordenes_reparacion', __name__)


# pass stuff to navbar through layout (used to search)
@ordenes_reparacion.context_processor
def layout():
	form = SearchForm()
	return dict(form=form)


@ordenes_reparacion.route("/all_ordenes_reparacion")
def all_ordenes_reparacion():	
	if current_user.role.role_name == 'Técnico':
		all_or = buscarLista(Orden_reparacion, current_user)
	else:	
		all_or = buscarLista(Orden_reparacion)
	filtrar_por = current_app.config["FILTROS_OR"]	
	return render_template('all_ordenes_reparacion.html', 
							lista=all_or, 
							filtrar_por = filtrar_por,
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
		equipo_id = extraerId(form.equipo.data)
		tecnico_id = extraerId(form.tecnico.data)
		if tecnico_id:
			estado_id = 2 # si hay tecnico asignado se pone en "asignada"
		else:
			estado_id = 1 # sino, "creada"
		orden_reparacion = Orden_reparacion(
							codigo=form.codigo.data, 
							content=form.content.data, 													
							author_or=current_user, 
							tecnico_id=tecnico_id,
							estado_id=estado_id,
							equipo_id=equipo_id)
		db.session.add(orden_reparacion)
		db.session.commit()
		flash(f'Orden de reparación {orden_reparacion.codigo} agregada!', 'success')
		return redirect(url_for('ordenes_reparacion.orden_reparacion', orden_reparacion_id=orden_reparacion.id))
	elif request.method == 'GET':
		equipment = Equipment.query.filter_by(id=equipment_id).first()
		if(equipment): # CARGA EL VALOR 'DEFAULT' EN SELECT si encuentra un equipo
			form.equipo.default = f'[{equipment.id}] {equipment.modelo_eq.nombre} ({equipment.owner.nombre} {equipment.owner.apellido})'
			form.process() 
	return render_template('create_orden_reparacion.html', 
												title='Agregar O.R.', 
												form=form, 
												legend="Crear órden de reparación")


@ordenes_reparacion.route("/update_orden_reparacion-<int:orden_reparacion_id>", methods=['GET', 'POST'])
@login_required
def update_orden_reparacion(orden_reparacion_id):
	orden_reparacion = Orden_reparacion.query.get_or_404(orden_reparacion_id)
	if orden_reparacion.author_or != current_user and orden_reparacion.tecnicoAsignado != current_user:
		flash(f'{orden_reparacion.author_or}, {current_user}, {current_user.role.role_name}','danger')
		abort(403) #http forbidden
	form = OrdenReparacionForm()
	if form.validate_on_submit():
		equipment_id = extraerId(form.equipo.data)
		user_id = extraerId(form.tecnico.data)
		orden_reparacion.tecnico_id = user_id
		if user_id:			
			orden_reparacion.estado_id = 2 # si se asignó un técnico, se cambia el estado
		else:
			orden_reparacion.estado_id = 1
		orden_reparacion.equipo_id = equipment_id				
		orden_reparacion.date_modified = dateFormat()
		orden_reparacion.codigo = form.codigo.data
		orden_reparacion.content = form.content.data
		db.session.commit()
		flash("Su órden de reparacion ha sido editada con éxito", 'success')
		return redirect(url_for('ordenes_reparacion.orden_reparacion', orden_reparacion_id=orden_reparacion.id))
	elif request.method == 'GET':
		# si no hay tecnico asignado lo deja vacio
		if orden_reparacion.tecnicoAsignado:
			form.tecnico.default = f'[{orden_reparacion.tecnicoAsignado.id}] {orden_reparacion.tecnicoAsignado.username} ({orden_reparacion.tecnicoAsignado.role.role_name})'
		form.equipo.default = f'[{orden_reparacion.equipo.id}] {orden_reparacion.equipo.modelo_eq.nombre} ({orden_reparacion.equipo.owner.nombre} {orden_reparacion.equipo.owner.apellido})'
		form.estado.default = f'[{orden_reparacion.estado.id}] {orden_reparacion.estado.descripcion}'
		form.process()
		form.codigo.data = orden_reparacion.codigo
		form.content.data = orden_reparacion.content	
	return render_template('create_orden_reparacion.html', 	
												title='Editar Orden reparacion', 
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
	return redirect(url_for('ordenes_reparacion.all_ordenes_reparacion', filterBy='estado_id', filterOrder='asc' ))


@ordenes_reparacion.route("/update_estado-<int:orden_reparacion_id>-<string:estado_descripcion>", methods=['GET'])
def update_estado(orden_reparacion_id, estado_descripcion):
	orden_reparacion = Orden_reparacion.query.get_or_404(orden_reparacion_id)
	estado_or = Estado_or.query.filter_by(descripcion=estado_descripcion).first()	
	orden_reparacion.date_modified = dateFormat()
	orden_reparacion.estado_id = estado_or.id
	db.session.commit()
	flash("La órden de reparación se ha actualizado", 'success')	
	return redirect(url_for('ordenes_reparacion.orden_reparacion', orden_reparacion_id=orden_reparacion.id))


@ordenes_reparacion.route("/reporte_or_tecnico")
def reporte_tecnico(user_id):
	if current_user.role.role_name == 'Técnico':
		all_or = buscarLista(Orden_reparacion, current_user)
	else:	
		all_or = buscarLista(Orden_reparacion)
	filtrar_por = current_app.config["FILTROS_OR"]	
	return render_template('reporte_tecnico.html', 
							lista=all_or, 
							filtrar_por = filtrar_por,
							title='Reporte Órdenes de reparación')