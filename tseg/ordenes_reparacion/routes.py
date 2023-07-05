# Orden_reparacions routes
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, current_app
from flask_login import current_user, login_required
from tseg import db
from tseg.models import Orden_reparacion, Equipment, User, Estado_or
from tseg.ordenes_reparacion.forms import OrdenReparacionForm

from tseg.users.utils import role_required, dateFormat, buscarLista, identificador_en_corchete


ordenes_reparacion = Blueprint('ordenes_reparacion', __name__)

@ordenes_reparacion.route("/all_ordenes_reparacion")
def all_ordenes_reparacion():	
	if current_user.role.role_name == 'Técnico':
		all_or = buscarLista(Orden_reparacion, current_user)
	else:	
		all_or = buscarLista(Orden_reparacion)
	orderBy = current_app.config["ORDER_OR"]	
	return render_template('all_ordenes_reparacion.html', 
							lista=all_or, 
							orderBy = orderBy,
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
		serie = identificador_en_corchete(form.equipo.data)		
		equipment = Equipment.query.filter_by(numSerie=serie).first()
		user = User.query.filter_by(id=form.tecnico.data).first()
		if user:
			estado_id = 2 # si hay tecnico asignado se pone en "asignada"
		else:
			estado_id = 1 # sino, "creada"
		orden_reparacion = Orden_reparacion(
							codigo=form.codigo.data, 
							content=form.content.data, 													
							author_or=current_user, 
							tecnicoAsignado=user,
							estado_id=estado_id,
							equipo=equipment)
		try:
			db.session.add(orden_reparacion)
			db.session.commit()
			flash(f'Orden de reparación {orden_reparacion.codigo} agregada!', 'success')
			return redirect(url_for('ordenes_reparacion.orden_reparacion', orden_reparacion_id=orden_reparacion.id))
		except Exception as err:
			flash(f'Ocurrió un error al intentar guardar los datos. Error: {err}', 'danger')
			return redirect(url_for('ordenes_reparacion.add_orden_reparacion', equipment_id=equipment.id))
	elif request.method == 'GET':
		equipment = Equipment.query.filter_by(id=equipment_id).first()
		if equipment: # CARGA EL VALOR 'DEFAULT' EN SELECT si encuentra un equipo
			form.equipo.default = equipment
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
		equipment = Equipment.query.filter_by(form.equipo.data).first()
		user = User.query.filter_by(form.tecnico.data).first()
		
		orden_reparacion.tecnico_id = user.id
		if user:			
			orden_reparacion.estado_id = 2 # si se asignó un técnico, se cambia el estado
		else:
			orden_reparacion.estado_id = 1
		orden_reparacion.equipo_id = equipment_id				
		orden_reparacion.date_modified = dateFormat()
		orden_reparacion.codigo = form.codigo.data
		orden_reparacion.content = form.content.data
		try:
			db.session.commit()
			flash("Su órden de reparacion ha sido editada con éxito", 'success')
			return redirect(url_for('ordenes_reparacion.orden_reparacion', orden_reparacion_id=orden_reparacion.id))
		except Exception as err:
			flash(f'Ocurrió un error al intentar guardar los datos. Error: {err}', 'danger')
			return redirect(url_for('ordenes_reparacion.update_orden_reparacion', orden_reparacion_id=orden_reparacion.id))
	elif request.method == 'GET':
		# si no hay tecnico asignado lo deja vacio
		if orden_reparacion.tecnicoAsignado:
			form.tecnico.default = orden_reparacion.tecnicoAsignado
		form.equipo.default = orden_reparacion.equipo
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


@ordenes_reparacion.route("/reporte_tecnico")
def reporte_tecnico():
	all_or = buscarLista(Orden_reparacion)
	orderBy = current_app.config["ORDER_OR"]	
	return render_template('reporte_tecnico.html', 
							lista=all_or, 
							orderBy = orderBy,
							title='Reporte Órdenes de reparación')