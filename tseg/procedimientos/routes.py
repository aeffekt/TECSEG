from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, current_app
from flask_login import current_user, login_required
from tseg import db
from tseg.models import Procedimiento, dateFormat
from tseg.procedimientos.forms import ProcedimientoForm
from tseg.users.utils import role_required, buscarLista, error_logger

procedimientos = Blueprint('procedimientos', __name__)


@login_required
@procedimientos.route("/all_procedimientos")
def all_procedimientos():	
	select_item = request.args.get('selectItem', '')
	if select_item:
		return redirect(url_for('procedimientos.procedimiento', procedimiento_id=select_item, 
														filterBy='date_modified',
														filterSort='desc'))		
	all_procedimientos = buscarLista(Procedimiento)
	orderBy = current_app.config["ORDER_PROCEDIMIENTOS"]
	item_type = 'Equipo'
	return render_template('all_procedimientos.html',
							lista=all_procedimientos,
							orderBy = orderBy,
							title='Procedimientos', 							
							item_type=item_type)


@procedimientos.route("/procedimiento-new", methods=['GET', 'POST'])
@role_required("Admin", "Técnico")
def add_procedimiento():
	form = ProcedimientoForm()	
	if form.validate_on_submit():
		try:
			procedimiento = Procedimiento(
							title=form.title.data,
							content=form.content.data,							
							user=current_user,
							user_edit=current_user,
							)
			db.session.add(procedimiento)
			db.session.commit()
			flash('Se ha guardado el procedimiento técnico!', 'success')
			return redirect(url_for('procedimientos.all_procedimientos', filterBy='date_modified', filterOrder='desc'))
		except Exception as e:
			error_logger(e)
			return redirect(url_for('procedimientos.add_procedimiento', procedimiento_id=procedimiento.id))
	return render_template('create_procedimiento.html', title='Nuevo Procedimiento', 
												form=form,												
												legend=f'Nuevo Procedimiento')


# ruteo de variables "procedimiento_id"
@procedimientos.route("/procedimiento-<int:procedimiento_id>")
@login_required
def procedimiento(procedimiento_id):
	procedimiento = Procedimiento.query.get_or_404(procedimiento_id)	
	return render_template("procedimiento.html", procedimiento=procedimiento)


@procedimientos.route("/procedimiento-<int:procedimiento_id>-update", methods=['GET', 'POST'])
@role_required("Admin", "Técnico")
def update_procedimiento(procedimiento_id):
	procedimiento = Procedimiento.query.get_or_404(procedimiento_id)	
	form = ProcedimientoForm(procedimiento)
	if form.validate_on_submit():	
		try:
			procedimiento.title = form.title.data
			procedimiento.content = form.content.data
			procedimiento.date_modified = dateFormat()
			procedimiento.user_edit = current_user
			db.session.commit()
			flash("El procedimiento ha sido modificado con éxito", 'success')
			return redirect(url_for('procedimientos.procedimiento', procedimiento_id=procedimiento.id))
		except Exception as e:
			error_logger(e)
			return redirect(url_for('procedimientos.update_procedimiento', procedimiento_id=procedimiento.id))
	elif request.method == 'GET':		
		form.title.data = procedimiento.title
		form.content.data = procedimiento.content
	return render_template('create_procedimiento.html',	title='Editar procedimiento', 
												form=form,
												legend="Editar procedimiento")


@procedimientos.route("/procedimiento-<int:procedimiento_id>-delete", methods=['POST'])
@role_required("Admin", "Técnico")
def delete_procedimiento(procedimiento_id):
	procedimiento = Procedimiento.query.get_or_404(procedimiento_id)	
	if procedimiento.user_id != current_user.id:
		abort(403)
	try:
		db.session.delete(procedimiento)
		db.session.commit()
		flash(f"El procedimiento '{procedimiento}' ha sido eliminado!", 'success')
		return redirect(url_for('procedimientos.all_procedimientos'))
	except Exception as e:
		error_logger(e)
		return redirect(url_for('procedimientos.procedimiento', procedimiento_id=procedimiento.id))
