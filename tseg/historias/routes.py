from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from tseg import db
from tseg.models import Historia, Equipment, dateFormat
from tseg.historias.forms import HistoriaForm
from tseg.users.utils import role_required, error_logger

historias = Blueprint('historias', __name__)

@historias.route("/historia-new-<string:equipment_id>", methods=['GET', 'POST'])
@role_required("Admin", "Técnico") # impide el acceso sin login
def add_historia(equipment_id):
	form = HistoriaForm()
	equipment = Equipment.query.get_or_404(equipment_id)
	if form.validate_on_submit():		
		historia = Historia(tipo_historia_id=form.tipo.data,
							title=form.title.data,
							content=form.content.data,
							eq_historia=equipment, 
							author_historia=current_user)
		try:
			db.session.add(historia)
			db.session.commit()
			flash('Se ha guardado la nueva Historia de equipo!', 'success')
			return redirect(url_for('equipments.equipment', equipment_id=equipment_id, filterBy='date_modified', filterOrder='desc'))
		except Exception as e:
			error_logger(e)
			return redirect(url_for('historias.add_historia', equipment_id=equipment.id))
	return render_template('create_historia.html', title='Nueva Historia', 
												form=form,
												equipment=equipment,
												legend=f'Nueva Historia: \
												{equipment.modelo} de \
												{equipment.detalle_trabajo.orden_trabajo.client.nombre} {equipment.detalle_trabajo.orden_trabajo.client.apellido}')


# ruteo de variables "historia_id"
@historias.route("/historia-<int:historia_id>")
@login_required
def historia(historia_id):
	historia = Historia.query.get_or_404(historia_id)	
	return render_template("historia.html", historia=historia)


@historias.route("/historia-<int:historia_id>-update", methods=['GET', 'POST'])
@role_required("Admin", "Técnico")
def update_historia(historia_id):
	historia = Historia.query.get_or_404(historia_id)
	if historia.author_historia != current_user:
		abort(403) #http forbidden
	form = HistoriaForm()
	if form.validate_on_submit():
		try:
			historia.tipo_historia_id = form.tipo.data
			historia.title = form.title.data
			historia.content = form.content.data
			historia.date_modified = dateFormat()		
			db.session.commit()
			flash("Su historia ha sido modificada con éxito", 'success')
			return redirect(url_for('historias.historia', historia_id=historia.id))
		except Exception as e:
			error_logger(e)
			return redirect(url_for('equipments.update_historia', historia_id=historia.id))
	elif request.method == 'GET':
		form.tipo.default = historia.tipo_historia_id
		form.process()
		form.title.data = historia.title
		form.content.data = historia.content
	return render_template('create_historia.html',	title='Editar historia', 
												form=form,
												legend="Editar historia")


@historias.route("/historia-<int:historia_id>-delete", methods=['POST'])
@role_required("Admin", "Técnico")
def delete_historia(historia_id):
	historia = Historia.query.get_or_404(historia_id)
	if historia.author_historia != current_user:
		abort(403)
	db.session.delete(historia)
	db.session.commit()
	flash("Su historia ha sido eliminada!", 'success')
	return redirect(url_for('equipments.equipment', equipment_id=historia.equipo_id, filterBy='date_modified', filterOrder='desc'))