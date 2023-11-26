# Orden_trabajo routes
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, current_app
from flask_login import current_user, login_required
from tseg import db
from tseg.models import Orden_trabajo, Client, Detalle_trabajo, dateFormat
from tseg.ordenes_trabajo.forms import OrdenTrabajoForm
from tseg.users.utils import role_required, buscarLista, error_logger


ordenes_trabajo = Blueprint('ordenes_trabajo', __name__)


@ordenes_trabajo.route("/all_ordenes_trabajo")
@login_required
def all_ordenes_trabajo():
	try:
		select_item = request.args.get('selectItem', '')
		if select_item:			
			return redirect(url_for('ordenes_trabajo.orden_trabajo', orden_trabajo_id=select_item))
	except Exception as err:
		flash(f'Ocurrió un error al intentar mostrar el Item.', 'warning')
		return redirect(url_for('ordenes_trabajo.all_ordenes_trabajo', orderBy='estado_id', orderOrder='asc'))
	all_ot = buscarLista(Orden_trabajo)
	orderBy = current_app.config["ORDER_OT"]
	item_type = 'Orden de Reparación'
	return render_template('all_ordenes_trabajo.html', 
							lista=all_ot, 
							orderBy = orderBy,
							title='Órdenes de Trabajo',
							item_type=item_type)


# ruteo de variables "Orden_trabajo_id"
@ordenes_trabajo.route("/orden_trabajo-<int:orden_trabajo_id>")
@login_required
def orden_trabajo(orden_trabajo_id):
	sistemas=[]
	select_item = request.args.get('selectItem')
	if select_item:		
		return redirect(url_for('detalles_trabajo.detalle_trabajo', detalle_trabajo_id=select_item))
	orden_trabajo = Orden_trabajo.query.get_or_404(orden_trabajo_id)
	detalles_trabajo =  buscarLista(Detalle_trabajo, orden_trabajo)	
	orderBy = current_app.config['ORDER_DETALLES_OT']
	for detalle in detalles_trabajo:
		for equipment in detalle.equipments:
			if equipment.sistema != None and equipment.sistema not in sistemas:
				sistemas.append(equipment.sistema)
	image_path = url_for("static", filename='models_pics/')
	# texto para toolbar
	item_type="Detalle de orden de Trabajo"	
	return render_template("orden_trabajo.html", title=f'O.T. {orden_trabajo}',
											orden_trabajo=orden_trabajo,
											legend="Ver Orden de Trabajo",
											orderBy = orderBy,
											lista=detalles_trabajo,											
											item_type=item_type,
											sistemas=sistemas,
											image_path=image_path
											)
	

@ordenes_trabajo.route("/add_orden_trabajo-<string:client_id>", methods=['GET','POST'] )
@role_required("Admin", "ServicioCliente", "Comercial")
def add_orden_trabajo(client_id):
	form = OrdenTrabajoForm()
	client = Client.query.filter_by(id=client_id).first()
	vieja_orden_trabajo = None
	# Si se llamo desde copiar OT, pasa el argunmento viaja OT
	copiar_orden_trabajo_id = request.args.get('copiar_orden_trabajo_id', '')
	if copiar_orden_trabajo_id:
		vieja_orden_trabajo = Orden_trabajo.query.get(copiar_orden_trabajo_id)	
	if form.validate_on_submit():
		try:
			orden_trabajo = Orden_trabajo(
							codigo=form.codigo.data, 
							content=form.content.data,
							notes=form.notes.data,
							client_id=form.client.data,
							estado_id=form.estado.data,
							author_ot=current_user)
			db.session.add(orden_trabajo)
			db.session.commit()
			#copia todos los detalles de la vieja OT en la nueva	
			if vieja_orden_trabajo:				
				detalles_trabajo = buscarLista(Detalle_trabajo, vieja_orden_trabajo)
				for dt in detalles_trabajo:
					nuevo_detalle_trabajo = Detalle_trabajo(content=dt.content,
															cantidad=dt.cantidad,
															orden_trabajo=orden_trabajo,
															author_detalle_trabajo=current_user)					
					db.session.add(nuevo_detalle_trabajo)
				db.session.commit()
			flash(f'Orden de Trabajo {orden_trabajo.codigo} agregada!', 'success')
			return redirect(url_for('ordenes_trabajo.orden_trabajo', orden_trabajo_id=orden_trabajo.id))
		except Exception as e:
			error_logger(e)
			return redirect(url_for('ordenes_trabajo.add_orden_trabajo', client_id=client_id))	
	if client: # CARGA EL VALOR 'DEFAULT' EN SELECT si se por arg client
		form.client.default = client.id
		form.process() 
		if vieja_orden_trabajo:
			form.content.data = vieja_orden_trabajo.content
	return render_template('create_orden_trabajo.html', 
												title='Registrar O.T.', 
												form=form, 
												legend="Registrar orden de Trabajo")


@ordenes_trabajo.route("/copy_orden_trabajo-<string:orden_trabajo_id>")
@role_required("Admin", "ServicioCliente", "Comercial")
def copy_orden_trabajo(orden_trabajo_id):
	orden_trabajo = Orden_trabajo.query.get_or_404(orden_trabajo_id)	
	return redirect(url_for('ordenes_trabajo.add_orden_trabajo', client_id=orden_trabajo.client.id, copiar_orden_trabajo_id=orden_trabajo.id))


@ordenes_trabajo.route("/update_orden_trabajo-<int:orden_trabajo_id>", methods=['GET', 'POST'])
@role_required("Admin", "ServicioCliente", "Comercial", "Técnico")
def update_orden_trabajo(orden_trabajo_id):
	orden_trabajo = Orden_trabajo.query.get_or_404(orden_trabajo_id)	
	form = OrdenTrabajoForm(orden_trabajo)
	if form.validate_on_submit():
		try:			
			orden_trabajo.client_id = form.client.data
			orden_trabajo.estado_id = form.estado.data
			orden_trabajo.date_modified = dateFormat()
			orden_trabajo.codigo = form.codigo.data
			orden_trabajo.content = form.content.data
			orden_trabajo.notes = form.notes.data
			db.session.commit()
			flash("Su orden de trabajo ha sido editada con éxito", 'success')
			return redirect(url_for('ordenes_trabajo.orden_trabajo', orden_trabajo_id=orden_trabajo.id))
		except Exception as e:
			error_logger(e)
			return redirect(url_for('ordenes_trabajo.update_orden_trabajo', orden_trabajo_id=orden_trabajo.id))
	elif request.method == 'GET':		
		form.client.default = orden_trabajo.client_id
		form.estado.default = orden_trabajo.estado.id
		form.process()
		form.codigo.data = orden_trabajo.codigo
		form.content.data = orden_trabajo.content	
	return render_template('create_orden_trabajo.html', 	
												title='Editar Orden trabajo', 
												form=form,
												legend="Editar Orden trabajo")


@ordenes_trabajo.route("/orden_trabajo-<int:orden_trabajo_id>-delete", methods=['POST'])
@role_required("Admin", "Comercial", "ServicioCliente")
def delete_orden_trabajo(orden_trabajo_id):
	orden_trabajo = Orden_trabajo.query.get_or_404(orden_trabajo_id)
	if orden_trabajo.author_ot != current_user:
		abort(403)
	try:
		for detalle_trabajo in orden_trabajo.detalles_trabajo:
			db.session.delete(detalle_trabajo)
		db.session.delete(orden_trabajo)
		db.session.commit()
		flash(f"La orden de trabajo {orden_trabajo.codigo} ha sido eliminada!", 'success')
		return redirect(url_for('ordenes_trabajo.all_ordenes_trabajo', orderBy='estado_id', orderOrder='asc'))
	except Exception as e:
		db.session.rollback() 
		flash("Ocurrió un error al intentar eliminar.", 'warning')		
		flash(f"Hay equipos asociados a la O.T. Debe borrarlos primero", 'warning')
		return redirect(url_for('ordenes_trabajo.orden_trabajo', orden_trabajo_id=orden_trabajo.id))	
