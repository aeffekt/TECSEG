# Orden_reparacions routes
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, current_app
from flask_login import current_user, login_required
from tseg import db
from tseg.models import Orden_reparacion
from tseg.ordenes_reparacion.forms import OrdenReparacionForm
from tseg.users.forms import SearchForm
from tseg.users.utils import role_required

ordenes_reparacion = Blueprint('ordenes_reparacion', __name__)



@ordenes_reparacion.route("/all_ordenes_reparacion")
def all_ordenes_reparacion():
	page = request.args.get('page', 1, type=int) # num pagina de mensajes
	all_or = Orden_reparacion.query.order_by(Orden_reparacion.date_created.desc()).paginate(page=page, per_page=current_app.config['PER_PAGE'])
	return render_template('all_ordenes_reparacion.html', 
							all_or=all_or, 
							title='Órdenes de reparación')

# ruteo de variables "Orden_reparacion_id"
@ordenes_reparacion.route("/orden_reparacion-<int:Orden_reparacion_id>")
def orden_reparacion(orden_reparacion_id):
	orden_reparacion = Orden_reparacion.query.get_or_404(Orden_reparacion_id)
	return render_template("orden_reparacion.html", orden_reparacion=post)


@ordenes_reparacion.route("/add_orden_reparacion-<string:equipment_id>", methods=['GET','POST'] )
@role_required("Admin", "Técnico", "ServicioCliente")
def add_orden_reparacion(equipment_id):
	form = OrdenReparacionForm()
	if form.validate_on_submit():		
		equipment = Equipment.query.filter_by(equipment_id=equipment_id).first()
		orden_reparacion = Orden_reparacion(title=form.title.data, 
							content=form.content.data, 
							author_eq=current_user, 
							equipment_id=equipment.id)
		db.session.add(orden_reparacion)
		db.session.commit()
		flash(f'Orden de reparación {orden_reparacion.title} agregada!', 'success')
		return redirect(url_for('ordenes_reparacion.orden_reparacion', orden_reparacion_id=orden_reparacion.id))
	elif request.method == 'GET':
		form.owner.choices = equipment.query.all()
		form.owner.default = equipment.query.filter_by(id=equipment_id).first()
		form.process() # CARGA EL VALOR 'DEFAULT' EN SELECT		
	return render_template('create_orden_reparacion.html', title='Agregar equipo', 
												form=form, legend="Agregar equipo")


@ordenes_reparacion.route("/orden_reparacion-<int:orden_reparacion_id>-update", methods=['GET', 'POST'])
@login_required
def update_orden_reparacion(orden_reparacion_id):
	orden_reparacion = Orden_reparacion.query.get_or_404(orden_reparacion_id)
	if orden_reparacion.author != current_user:
		abort(403) #http forbidden
	form = Orden_reparacionForm()
	if form.validate_on_submit():
		orden_reparacion.content = form.content.data
		db.session.commit()
		flash("Su Orden_reparacion ha sido editado con éxito", 'success')
		return redirect(url_for('ordenes_reparacion.orden_reparacion', orden_reparacion_id=orden_reparacion.id))
	elif request.method == 'GET':
		form.content.data = orden_reparacion.content
	return render_template('create_orden_reparacion.html', 	title='Editar Orden reparacion', 
												form=form,
												legend="Editar Orden reparacion")

@ordenes_reparacion.route("/orden_reparacion-<int:orden_reparacion_id>-delete", methods=['Orden_reparacion'])
@login_required
def delete_orden_reparacion(orden_reparacion_id):
	Orden_reparacion = Orden_reparacion.query.get_or_404(orden_reparacion_id)
	if Orden_reparacion.author != current_user:
		abort(403)
	db.session.delete(Orden_reparacion)
	db.session.commit()
	flash("Su Orden reparacion ha sido eliminada!", 'success')
	return redirect(url_for('ordenes_reparacion.all_ordenes_reparacion'))