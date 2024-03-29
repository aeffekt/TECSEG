from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from tseg import db
from tseg.models import Detalle_reparacion, Orden_reparacion, dateFormat
from tseg.detalles_reparacion.forms import DetalleReparacionForm
from tseg.users.utils import role_required, error_logger

detalles_reparacion = Blueprint('detalles_reparacion', __name__)

@detalles_reparacion.route("/detalle-new-<string:orden_reparacion_id>", methods=['GET', 'POST'])
@role_required("Admin", "Técnico")
def add_detalle_reparacion(orden_reparacion_id):
	form = DetalleReparacionForm()
	orden_reparacion = Orden_reparacion.query.get_or_404(orden_reparacion_id)
	if form.validate_on_submit():
		try:
			detalle_reparacion = Detalle_reparacion(content=form.content.data,
							orden_reparacion=orden_reparacion, 
							author_detalle_reparacion=current_user)		
			db.session.add(detalle_reparacion)
			db.session.commit()
			flash('Se ha guardado el nuevo detalle de reparación!', 'success')
			return redirect(url_for('ordenes_reparacion.orden_reparacion', orden_reparacion_id=orden_reparacion_id, filterBy='date_modified', filterOrder='desc'))
		except Exception as e:
			error_logger(e)
			return redirect(url_for('detalles_reparacion.add_detalle_reparacion', orden_reparacion_id=orden_reparacion.id))
	return render_template('create_detalle_reparacion.html', title='Nueva detalle_reparacion', 
												form=form,
												orden_reparacion=orden_reparacion,
												legend=f'Nuevo detalle de reparación de la O.R. {orden_reparacion.codigo}'
												)


# ruteo de variables "detalle_reparacion_id"
@detalles_reparacion.route("/detalle-reparacion-<int:detalle_reparacion_id>")
@login_required
def detalle_reparacion(detalle_reparacion_id):
	detalle_reparacion = Detalle_reparacion.query.get_or_404(detalle_reparacion_id)	
	return render_template("detalle_reparacion.html", detalle_reparacion=detalle_reparacion)


@detalles_reparacion.route("/detalle-<int:detalle_reparacion_id>-update", methods=['GET', 'POST'])
@role_required("Admin", "Técnico")
def update_detalle_reparacion(detalle_reparacion_id):
	detalle_reparacion = Detalle_reparacion.query.get_or_404(detalle_reparacion_id)
	if detalle_reparacion.author_detalle_reparacion != current_user:
		abort(403) #http forbidden
	form = DetalleReparacionForm()
	if form.validate_on_submit():
		try:
			detalle_reparacion.content = form.content.data
			detalle_reparacion.date_modified = dateFormat()		
			db.session.commit()
			flash("Su detalle de reparación ha sido modificado con éxito", 'success')
			return redirect(url_for('ordenes_reparacion.orden_reparacion', orden_reparacion_id=detalle_reparacion.orden_reparacion.id))
		except Exception as e:			
			error_logger(e)			
			return redirect(url_for('ordenes_reparacions.update_detalle_reparacion', detalle_reparacion_id=detalle_reparacion.id))
	elif request.method == 'GET':		
		form.content.data = detalle_reparacion.content
	return render_template('create_detalle_reparacion.html',	title='Editar detalle de reparación', 
												form=form,
												legend="Editar detalle de reparación")

@detalles_reparacion.route("/detalle-<int:detalle_reparacion_id>-delete", methods=['POST'])
@role_required("Admin", "Técnico")
def delete_detalle_reparacion(detalle_reparacion_id):
	detalle_reparacion = Detalle_reparacion.query.get_or_404(detalle_reparacion_id)
	# se guarda la or id para que no de error al no encontrar el detalle en redirect
	or_id = detalle_reparacion.orden_reparacion.id
	if detalle_reparacion.author_detalle_reparacion != current_user:
		abort(403)
	db.session.delete(detalle_reparacion)
	db.session.commit()
	flash("Su detalle de reparación ha sido eliminado!", 'success')
	return redirect(url_for('ordenes_reparacion.orden_reparacion', orden_reparacion_id=or_id, filterBy='date_modified', filterOrder='desc'))
