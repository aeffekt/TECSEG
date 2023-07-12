# Orden_reparacions routes
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, current_app
from flask_login import current_user, login_required
from tseg import db
from tseg.models import Orden_reparacion, Equipment, User, Estado_or, Role
from tseg.ordenes_reparacion.forms import OrdenReparacionForm
from sqlalchemy import func
from tseg.users.utils import role_required, dateFormat, buscarLista, identificador_en_corchete


ordenes_reparacion = Blueprint('ordenes_reparacion', __name__)

@ordenes_reparacion.route("/all_ordenes_reparacion")
def all_ordenes_reparacion():
	try:
		select_item = request.args.get('selectItem', '')
		if select_item:
			codigo_str = select_item.split()[0]
			# divide el __repr__ y obtiene el código en pos 2		
			orden = Orden_reparacion.query.filter_by(codigo=codigo_str).first()
			return redirect(url_for('ordenes_reparacion.orden_reparacion', orden_reparacion_id=orden.id))
	except Exception as err:
		flash(f'Ocurrió un error al intentar mostrar el Item. Error: {err}', 'danger')
		return redirect(url_for('ordenes_reparacion.all_ordenes_reparacion'))
	if current_user.role.role_name == 'Técnico':
		all_or = buscarLista(Orden_reparacion, current_user)
	else:	
		all_or = buscarLista(Orden_reparacion)
	orderBy = current_app.config["ORDER_OR"]
	item_type = 'Órden de Reparación'
	return render_template('all_ordenes_reparacion.html', 
							lista=all_or, 
							orderBy = orderBy,
							title='Órdenes de reparación',
							item_type=item_type)


# ruteo de variables "Orden_reparacion_id"
@ordenes_reparacion.route("/orden_reparacion-<int:orden_reparacion_id>")
def orden_reparacion(orden_reparacion_id):
	orden_reparacion = Orden_reparacion.query.get_or_404(orden_reparacion_id)
	return render_template("orden_reparacion.html", 
							orden_reparacion=orden_reparacion, 
							title=f'O.R. {orden_reparacion}',)


@ordenes_reparacion.route("/add_orden_reparacion-<string:equipment_id>", methods=['GET','POST'] )
@role_required("Admin", "ServicioCliente")
def add_orden_reparacion(equipment_id):
	form = OrdenReparacionForm()
	if form.validate_on_submit():		
		numSerie = identificador_en_corchete(form.equipo.data)
		equipment = Equipment.query.filter_by(numSerie=numSerie).first()
		username = form.tecnico.data.split()[0]  # Obtener el nombre de usuario del valor __repr__		
		user = User.query.filter_by(username=username).first()
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
		flash(f'Solo el autor {orden_reparacion.author_or} o un usuario "Admin" puede editar esta O.R.','warning')
		abort(403) #http forbidden
	form = OrdenReparacionForm(orden_reparacion)
	if form.validate_on_submit():		
		numSerie = identificador_en_corchete(form.equipo.data)
		equipment = Equipment.query.filter_by(numSerie=numSerie).first()
		username = form.tecnico.data.split()[0]  # Obtener el nombre de usuario del valor __repr__		
		user = User.query.filter_by(username=username).first()
		if user:			
			orden_reparacion.estado_id = 2 # si se asignó un técnico, se cambia el estado
		else:
			orden_reparacion.estado_id = 1
		orden_reparacion.tecnicoAsignado = user
		orden_reparacion.equipo = equipment
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