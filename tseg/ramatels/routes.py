from flask import render_template, request, Blueprint, flash, redirect, url_for, current_app
from flask_login import login_required
from tseg.models import Ramatel
from tseg.ramatels.forms import RamatelForm
from tseg.users.utils import role_required, buscarLista
from tseg import db


ramatels = Blueprint('ramatels', __name__)

@ramatels.route("/all_ramatels")
def all_ramatels():
	all_ramatels = buscarLista(Ramatel)	
	orderBy = current_app.config['ORDER_RAMATEL']
	return render_template('all_ramatels.html', 
							lista=all_ramatels,
							orderBy=orderBy,
							title='ramatel de equipo')


@ramatels.route("/ramatel-<int:ramatel_id>-update", methods=['GET', 'POST'])
@login_required
def ramatel(ramatel_id):
	ramatel = Ramatel.query.get_or_404(ramatel_id)
	form = RamatelForm()
	if form.validate_on_submit():		
		ramatel.codigo = form.codigo.data
		ramatel.modelo = form.modelo.data
		try:	
			db.session.commit()
			flash(f"El codigo {ramatel.codigo} ha sido actualizado.", 'success')
			return redirect(url_for('ramatels.ramatel', ramatel_id=ramatel.id))
		except Exception as err:
			flash(f'Ocurrió un error al intentar guardar los datos. Error: {err}', 'danger')
			return redirect(url_for('ramatel.ramatel', ramatel_id=ramatel.id))
	elif request.method == 'GET':		
		form.codigo.data = ramatel.codigo
		form.modelo.data = ramatel.modelo
	return render_template('ramatel.html',
						title='Código Ramatel',						
						form=form,
						ramatel=ramatel)


@ramatels.route("/add_ramatel", methods=['GET','POST'] )
@role_required("Admin", "Técnico")
def add_ramatel():
	form = RamatelForm()
	if form.validate_on_submit():		
		ramatel = Ramatel(codigo=form.codigo.data,
						modelo=form.modelo.data)
		try:
			db.session.add(ramatel)
			db.session.commit()
			flash(f'Código ramatel {ramatel.codigo} agregado!', 'success')
			return redirect(url_for('ramatels.all_ramatels', ramatel_id=ramatel.id))
		except Exception as err:
			flash(f'Ocurrió un error al intentar guardar los datos. Error: {err}', 'danger')
			return redirect(url_for('ramatels.add_ramatel'))
	else:
		return render_template('create_ramatel.html', title='Agregar código', 
												form=form, legend="Agregar código Ramatel")


@ramatels.route("/ramatel-<int:ramatel_id>-delete", methods=['GET', 'POST'])
@role_required("Admin", "Técnico")
def delete_ramatel(ramatel_id):
	ramatel = Ramatel.query.get_or_404(ramatel_id)
	db.session.delete(ramatel)
	db.session.commit()
	flash("El código ramatel ha sido eliminado!", 'success')
	return redirect(url_for('ramatels.all_ramatels'))