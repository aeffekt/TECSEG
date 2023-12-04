# Orden_reparacions routes
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, current_app
from flask_login import current_user, login_required
from tseg import db
from tseg.models import Orden_reparacion, Equipment, User, Estado_or, Detalle_reparacion, dateFormat
from tseg.ordenes_reparacion.forms import OrdenReparacionForm
from tseg.users.utils import role_required, buscarLista, error_logger


ordenes_reparacion = Blueprint('ordenes_reparacion', __name__)

@ordenes_reparacion.route("/all_ordenes_reparacion")
@login_required
def all_ordenes_reparacion():
	try:
		select_item = request.args.get('selectItem', '')
		if select_item:			
			return redirect(url_for('ordenes_reparacion.orden_reparacion', orden_reparacion_id=select_item))
	except Exception as err:
		flash(f'Ocurrió un error al intentar mostrar el Item. Error: {err}', 'danger')
		return redirect(url_for('ordenes_reparacion.all_ordenes_reparacion'))
	if current_user.role.role_name == 'Técnico':
		all_or = buscarLista(Orden_reparacion, current_user)
	else:	
		all_or = buscarLista(Orden_reparacion)
	orderBy = current_app.config["ORDER_OR"]
	item_type = 'Orden de Reparación'
	return render_template('all_ordenes_reparacion.html', 
							lista=all_or, 
							orderBy = orderBy,
							title='Órdenes de reparación',
							item_type=item_type)


# ruteo de variables "Orden_reparacion_id"
@ordenes_reparacion.route("/orden_reparacion-<int:orden_reparacion_id>")
@login_required
def orden_reparacion(orden_reparacion_id):
	select_item = request.args.get('selectItem')
	if select_item:		
		return redirect(url_for('detalles_reparacion.detalle_reparacion', detalle_reparacion_id=select_item))
	orden_reparacion = Orden_reparacion.query.get_or_404(orden_reparacion_id)
	detalles_reparacion =  buscarLista(Detalle_reparacion, orden_reparacion)	
	orderBy = current_app.config['ORDER_DETALLES_OT']	
	# texto para toolbar
	item_type="Detalle de reparación"	
	return render_template("orden_reparacion.html", title=f'O.R. {orden_reparacion}',
											orden_reparacion=orden_reparacion,
											legend="Ver Orden de Reparación",
											orderBy = orderBy,
											lista=detalles_reparacion,											
											item_type=item_type,	
											)
	

@ordenes_reparacion.route("/add_orden_reparacion-<string:equipment_id>", methods=['GET','POST'] )
@role_required("Admin", "ServicioCliente", "Técnico")
def add_orden_reparacion(equipment_id):
	form = OrdenReparacionForm()
	if form.validate_on_submit():
		try:		
			user = User.query.get(form.tecnico.data)
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
								equipo_id=form.equipo.data)		
			db.session.add(orden_reparacion)
			db.session.commit()
			flash(f'Orden de reparación {orden_reparacion.codigo} agregada!', 'success')
			return redirect(url_for('ordenes_reparacion.orden_reparacion', orden_reparacion_id=orden_reparacion.id))
		except Exception as e:
			error_logger(e)
			return redirect(url_for('ordenes_reparacion.add_orden_reparacion', equipment_id=equipment.id))	
	equipment = Equipment.query.filter_by(id=equipment_id).first()
	if equipment: # CARGA EL VALOR 'DEFAULT' EN SELECT si encuentra un equipo
		form.equipo.default = equipment.id
		form.process() 
	return render_template('create_orden_reparacion.html', 
												title='Registrar O.R.', 
												form=form, 
												legend="Registrar orden de reparación")


@ordenes_reparacion.route("/update_orden_reparacion-<int:orden_reparacion_id>", methods=['GET', 'POST'])
@role_required("Admin", "ServicioCliente", "Técnico")
def update_orden_reparacion(orden_reparacion_id):
	orden_reparacion = Orden_reparacion.query.get_or_404(orden_reparacion_id)
	if orden_reparacion.author_or != current_user\
		and orden_reparacion.tecnicoAsignado != current_user\
		and current_user.role.role_name != "Admin":
		flash(f'Solo el autor {orden_reparacion.author_or} o un usuario "Admin" puede editar esta O.R.','warning')
		abort(403) #http forbidden
	form = OrdenReparacionForm(orden_reparacion)
	if form.validate_on_submit():
		try:
			user = User.query.get(form.tecnico.data)
			if user:			
				orden_reparacion.estado_id = 2 # si se asignó un técnico, se cambia el estado
			else:
				orden_reparacion.estado_id = 1
			orden_reparacion.tecnicoAsignado = user
			orden_reparacion.equipo_id = form.equipo.data
			orden_reparacion.date_modified = dateFormat()
			orden_reparacion.codigo = form.codigo.data
			orden_reparacion.content = form.content.data
			db.session.commit()
			flash("Su Orden de Reparación ha sido editada con éxito", 'success')
			return redirect(url_for('ordenes_reparacion.orden_reparacion', orden_reparacion_id=orden_reparacion.id))
		except Exception as e:
			error_logger(e)
			return redirect(url_for('ordenes_reparacion.update_orden_reparacion', orden_reparacion_id=orden_reparacion.id))
	elif request.method == 'GET':		
		form.tecnico.default = orden_reparacion.tecnico_id
		form.equipo.default = orden_reparacion.equipo_id	
		form.process()
		form.codigo.data = orden_reparacion.codigo
		form.content.data = orden_reparacion.content	
	return render_template('create_orden_reparacion.html', 	
												title='Editar Orden reparacion', 
												form=form,
												legend="Editar Orden reparacion")


@ordenes_reparacion.route("/orden_reparacion-<int:orden_reparacion_id>-delete", methods=['POST'])
@role_required("Admin", "ServicioCliente")
def delete_orden_reparacion(orden_reparacion_id):
	orden_reparacion = Orden_reparacion.query.get_or_404(orden_reparacion_id)
	if orden_reparacion.author_or != current_user:
		abort(403)
	# elimina los detalles de la O.R.
	for detalle in orden_reparacion.detalles_reparacion:
		db.session.delete(detalle)
	db.session.delete(orden_reparacion)
	db.session.commit()
	flash(f"La Orden de Reparación {orden_reparacion.codigo} ha sido eliminada!", 'success')
	return redirect(url_for('ordenes_reparacion.all_ordenes_reparacion', filterBy='estado_id', filterOrder='asc' ))


@ordenes_reparacion.route("/update_estado-<int:orden_reparacion_id>-<string:estado_descripcion>", methods=['GET'])
@role_required("Admin", "ServicioCliente", "Técnico")
def update_estado(orden_reparacion_id, estado_descripcion):
	orden_reparacion = Orden_reparacion.query.get_or_404(orden_reparacion_id)
	estado_or = Estado_or.query.filter_by(descripcion=estado_descripcion).first()	
	orden_reparacion.date_modified = dateFormat()
	orden_reparacion.estado_id = estado_or.id
	db.session.commit()
	flash("La Orden de Reparación se ha actualizado", 'success')	
	return redirect(url_for('ordenes_reparacion.orden_reparacion', orden_reparacion_id=orden_reparacion.id))
