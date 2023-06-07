from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from tseg import db
from tseg.models import Eq_detail, Equipment
from tseg.eq_details.forms import Eq_detailForm
from tseg.users.forms import SearchForm

eq_details = Blueprint('eq_details', __name__)

@eq_details.context_processor
def layout():
	form = SearchForm()
	return dict(form=form)

@eq_details.route("/eq_detail-new-<string:equipment_id>", methods=['GET', 'POST'])
@login_required # impide el acceso sin login
def new_eq_detail(equipment_id):
	form = Eq_detailForm()
	equipment = Equipment.query.get_or_404(equipment_id)	
	if form.validate_on_submit():		
		eq_detail = Eq_detail(title=form.title.data,
							content=form.content.data,
							equipo=equipment, 
							author_detalle=current_user)
		db.session.add(eq_detail)
		db.session.commit()
		historias = Eq_detail.query.filter_by(equipment_id=equipment_id).order_by(Eq_detail.date_modified.desc())
		flash('Se ha guardado la nueva Historia de equipo!', 'success')
		return redirect(url_for('equipments.equipment', equipment_id=equipment_id))
	return render_template('create_eq_detail.html', title='Nueva Historia', 
												form=form,
												equipment=equipment,
												legend=f'Nueva Historia del equipo: {equipment.title}')


# ruteo de variables "eq_detail_id"
@eq_details.route("/eq_detail-<int:eq_detail_id>")
def eq_detail(eq_detail_id):
	eq_detail = Eq_detail.query.get_or_404(eq_detail_id)
	return render_template("eq_detail.html", eq_detail=eq_detail)


@eq_details.route("/eq_detail-<int:eq_detail_id>-update", methods=['GET', 'POST'])
@login_required
def update_eq_detail(eq_detail_id):
	eq_detail = Eq_detail.query.get_or_404(eq_detail_id)
	if eq_detail.author_detalle != current_user:
		abort(403) #http forbidden
	form = Eq_detailForm()
	if form.validate_on_submit():
		eq_detail.title = form.title.data
		eq_detail.content = form.content.data
		db.session.commit()
		flash("Su historia ha sido modificada con éxito", 'success')
		return redirect(url_for('eq_details.eq_detail', eq_detail_id=eq_detail.id))
	elif request.method == 'GET':
		form.title.data = eq_detail.title
		form.content.data = eq_detail.content
	return render_template('create_eq_detail.html',	title='Editar historia', 
												form=form,
												legend="Editar historia")

@eq_details.route("/eq_detail-<int:eq_detail_id>-delete", methods=['POST'])
@login_required
def delete_eq_detail(eq_detail_id):
	eq_detail = Eq_detail.query.get_or_404(eq_detail_id)
	if eq_detail.author_detalle != current_user:
		abort(403)
	db.session.delete(eq_detail)
	db.session.commit()
	flash("Su historia ha sido eliminada!", 'success')
	return redirect(url_for('equipments.equipment', equipment_id=eq_detail.equipment_id))