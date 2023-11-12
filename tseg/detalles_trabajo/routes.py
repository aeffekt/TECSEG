from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, current_app
from flask_login import current_user, login_required
from tseg import db
from tseg.models import Detalle_trabajo, Orden_trabajo, Equipment
from tseg.detalles_trabajo.forms import DetalleTrabajoForm
from tseg.users.utils import dateFormat, role_required, buscarLista

detalles_trabajo = Blueprint('detalles_trabajo', __name__)

@detalles_trabajo.route("/detalle-ot-nuevo-<string:orden_trabajo_id>", methods=['GET', 'POST'])
@login_required
def add_detalle_trabajo(orden_trabajo_id):
	form = DetalleTrabajoForm()
	orden_trabajo = Orden_trabajo.query.get_or_404(orden_trabajo_id)
	if form.validate_on_submit():		
		detalle_trabajo = Detalle_trabajo(content=form.content.data,
									cantidad=form.cantidad.data,
									orden_trabajo=orden_trabajo,
									author_detalle_trabajo=current_user)
		try:
			db.session.add(detalle_trabajo)
			db.session.commit()
			flash('Se ha guardado la nueva detalle de orden de trabajo!', 'success')
			return redirect(url_for('ordenes_trabajo.orden_trabajo', orden_trabajo_id=orden_trabajo.id, filterBy='date_modified', filterOrder='desc'))
		except Exception as err:
			flash(f'Ocurrió un error al intentar guardar los datos. Error: {err}', 'danger')
			return redirect(url_for('detalles_trabajo.add_detalle_trabajo', orden_trabajo_id=orden_trabajo.id))
	
	return render_template('create_detalle_trabajo.html', title='Nuevo detalle de trabajo', 
												form=form,
												orden_trabajo=orden_trabajo,
												legend=f'Nuevo detalle de la O.T. {orden_trabajo.codigo}'
												)


# ruteo de variables "detalle_trabajo_id"
@detalles_trabajo.route("/detalle-trabajo-<int:detalle_trabajo_id>")
@login_required
def detalle_trabajo(detalle_trabajo_id):
	detalle_trabajo = Detalle_trabajo.query.get_or_404(detalle_trabajo_id)
	equipments =  buscarLista(Equipment, detalle_trabajo)	
	orderBy = current_app.config['ORDER_EQUIPOS']	
	# texto para toolbar
	item_type="Equipos"	
	image_path = url_for("static", filename='models_pics/')
	return render_template("detalle_trabajo.html", title='Detalle de trabajo',
											legend="Ver equipo",
											orderBy = orderBy,
											lista=equipments,
											item_type=item_type,
											image_path=image_path,
											detalle_trabajo=detalle_trabajo)


@detalles_trabajo.route("/detalle-trabajo-<int:detalle_trabajo_id>-update", methods=['GET', 'POST'])
@login_required
def update_detalle_trabajo(detalle_trabajo_id):
	detalle_trabajo = Detalle_trabajo.query.get_or_404(detalle_trabajo_id)	
	form = DetalleTrabajoForm()
	if form.validate_on_submit():		
		detalle_trabajo.content = form.content.data
		detalle_trabajo.cantidad = form.cantidad.data
		detalle_trabajo.date_modified = dateFormat()
		try:
			db.session.commit()
			flash("Su detalle de trabajo ha sido modificado con éxito", 'success')
			return redirect(url_for('detalles_trabajo.detalle_trabajo', detalle_trabajo_id=detalle_trabajo.id))
		except Exception as err:
			flash(f'Ocurrió un error al intentar guardar los datos. Error: {err}', 'danger')
			return redirect(url_for('ordenes_trabajos.update_detalle_trabajo', detalle_trabajo_id=detalle_trabajo.id))
		
	form.content.data = detalle_trabajo.content
	form.cantidad.data = detalle_trabajo.cantidad
	return render_template('create_detalle_trabajo.html',	title='Editar detalle de trabajo', 
												form=form,
												legend="Editar detalle de trabajo")


@detalles_trabajo.route("/detalle-trabajo-<int:detalle_trabajo_id>-delete", methods=['POST'])
@login_required
def delete_detalle_trabajo(detalle_trabajo_id):	
	detalle_trabajo = Detalle_trabajo.query.get_or_404(detalle_trabajo_id)
	# se guarda la ot id para que no de error al no encontrar el detalle en redirect
	or_id = detalle_trabajo.orden_trabajo.id
	if detalle_trabajo.author_detalle_trabajo != current_user:
		abort(403)
	try:
		db.session.delete(detalle_trabajo)
		db.session.commit()
		flash("El detalle de trabajo ha sido eliminado!", 'success')
		return redirect(url_for('ordenes_trabajo.orden_trabajo', orden_trabajo_id=or_id, filterBy='date_modified', filterOrder='desc'))
	except Exception as e:
		db.session.rollback() 
		flash("Ocurrió un error al intentar eliminar.", 'warning')		
		flash(f"{e}", 'warning')
		return redirect(url_for('detalles_trabajo.detalle_trabajo', detalle_trabajo_id=detalle_trabajo.id))	