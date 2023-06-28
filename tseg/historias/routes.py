from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from tseg import db
from tseg.models import Historia, Equipment
from tseg.historias.forms import HistoriaForm
from tseg.users.forms import SearchForm
from tseg.users.utils import extraerId, dateFormat

historias = Blueprint('historias', __name__)

@historias.context_processor
def layout():
	form = SearchForm()
	return dict(form=form)

@historias.route("/historia-new-<string:equipment_id>", methods=['GET', 'POST'])
@login_required # impide el acceso sin login
def add_historia(equipment_id):
	form = HistoriaForm()
	equipment = Equipment.query.get_or_404(equipment_id)
	if form.validate_on_submit():
		tipologia_id = extraerId(form.tipo.data)
		historia = Historia(tipologia_id=tipologia_id,
							title=form.title.data,
							content=form.content.data,
							equipo_historia=equipment, 
							author_historia=current_user)
		db.session.add(historia)
		db.session.commit()
		flash('Se ha guardado la nueva Historia de equipo!', 'success')
		return redirect(url_for('equipments.equipment', equipment_id=equipment_id))
	return render_template('create_historia.html', title='Nueva Historia', 
												form=form,
												equipment=equipment,
												legend=f'Nueva Historia del equipo: {equipment.modelo_eq.nombre}')


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
		db.session.commit()
		flash("Su historia ha sido modificada con éxito", 'success')
		return redirect(url_for('historias.historia', historia_id=historia.id))
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
	return redirect(url_for('equipments.equipment', equipment_id=historia.equipment_id))