from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from tseg import db
from tseg.models import Historia, Equipment
from tseg.historias.forms import HistoriaForm
from tseg.users.utils import identificador_en_corchete, dateFormat

historias = Blueprint('historias', __name__)

@historias.route("/historia-new-<string:equipment_id>", methods=['GET', 'POST'])
@login_required # impide el acceso sin login
def add_historia(equipment_id):
	form = HistoriaForm()
	equipment = Equipment.query.get_or_404(equipment_id)
	if form.validate_on_submit():
		tipologia_id = identificador_en_corchete(form.tipo.data)
		historia = Historia(tipologia_id=tipologia_id,
							title=form.title.data,
							content=form.content.data,
							equipo_historia=equipment, 
							author_historia=current_user)
		try:
			db.session.add(historia)
			db.session.commit()
			flash('Se ha guardado la nueva Historia de equipo!', 'success')
			return redirect(url_for('equipments.equipment', equipment_id=equipment_id, filterBy='date_modified', filterOrder='desc'))
		except Exception as err:
			flash(f'Ocurrió un error al intentar guardar los datos. Error: {err}', 'danger')
			return redirect(url_for('historias.add_historia', equipment_id=equipment.id))
	return render_template('create_historia.html', title='Nueva Historia', 
												form=form,
												equipment=equipment,
												legend=f'Nueva Historia: \
												{equipment.modelo_eq.nombre} de \
												{equipment.owner.nombre} {equipment.owner.apellido}')


# ruteo de variables "historia_id"
@historias.route("/historia-<int:historia_id>")
def historia(historia_id):
	historia = Historia.query.get_or_404(historia_id)	
	return render_template("historia.html", historia=historia)


@historias.route("/historia-<int:historia_id>-update", methods=['GET', 'POST'])
@login_required
def update_historia(historia_id):
	historia = Historia.query.get_or_404(historia_id)
	if historia.author_historia != current_user:
		abort(403) #http forbidden
	form = HistoriaForm()
	if form.validate_on_submit():
		historia.title = form.title.data
		historia.content = form.content.data
		historia.date_modified = dateFormat()
		try:
			db.session.commit()
			flash("Su historia ha sido modificada con éxito", 'success')
			return redirect(url_for('historias.historia', historia_id=historia.id))
		except Exception as err:
			flash(f'Ocurrió un error al intentar guardar los datos. Error: {err}', 'danger')
			return redirect(url_for('equipments.update_historia', historia_id=historia.id))
	elif request.method == 'GET':
		form.title.data = historia.title
		form.content.data = historia.content
	return render_template('create_historia.html',	title='Editar historia', 
												form=form,
												legend="Editar historia")

@historias.route("/historia-<int:historia_id>-delete", methods=['POST'])
@login_required
def delete_historia(historia_id):
	historia = Historia.query.get_or_404(historia_id)
	if historia.author_historia != current_user:
		abort(403)
	db.session.delete(historia)
	db.session.commit()
	flash("Su historia ha sido eliminada!", 'success')
	return redirect(url_for('equipments.equipment', equipment_id=historia.equipo_id, filterBy='date_modified', filterOrder='desc'))