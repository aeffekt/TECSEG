from flask import render_template, request, Blueprint, flash, redirect, url_for, current_app
from flask_login import login_required
from tseg.models import Homologacion
from tseg.homologaciones.forms import HomologacionForm
from tseg.users.utils import role_required, buscarLista
from tseg import db


homologaciones = Blueprint('homologaciones', __name__)

@homologaciones.route("/all_homologaciones")
@login_required
def all_homologaciones():
	select_item = request.args.get('selectItem', '')
	if select_item:		
		return redirect(url_for('homologaciones.homologacion', homologacion_id=select_item))
	all_homologaciones = buscarLista(Homologacion)	
	orderBy = current_app.config['ORDER_HOMOLOGACION']
	item_type = 'Homologación'
	return render_template('all_homologaciones.html', 
							lista=all_homologaciones,
							orderBy=orderBy,
							title='Homologaciónes',
							item_type=item_type)


@homologaciones.route("/homologacion-<int:homologacion_id>-update", methods=['GET', 'POST'])
@login_required
def homologacion(homologacion_id):
	homologacion = Homologacion.query.get_or_404(homologacion_id)
	form = HomologacionForm(homologacion)
	if form.validate_on_submit():		
		homologacion.codigo = form.codigo.data
		homologacion.modelo = form.modelo.data
		try:	
			db.session.commit()
			flash(f"El codigo {homologacion.codigo} ha sido actualizado.", 'success')
			return redirect(url_for('homologaciones.homologacion', homologacion_id=homologacion.id))
		except Exception as err:
			flash(f'Ocurrió un error al intentar guardar los datos. Error: {err}', 'danger')
			return redirect(url_for('homologacion.homologacion', homologacion_id=homologacion.id))
	elif request.method == 'GET':		
		form.codigo.data = homologacion.codigo
		form.modelo.data = homologacion.modelo
	return render_template('homologacion.html',
						title='Código homologacion',						
						form=form,
						homologacion=homologacion)


@homologaciones.route("/add_homologacion", methods=['GET','POST'] )
@role_required("Admin", "Comercial")
def add_homologacion():
	form = HomologacionForm()
	if form.validate_on_submit():		
		homologacion = Homologacion(
						codigo=form.codigo.data,
						modelo=form.modelo.data)
		try:
			db.session.add(homologacion)
			db.session.commit()
			flash(f'Código homologacion {homologacion.codigo} agregado!', 'success')
			return redirect(url_for('homologaciones.all_homologaciones', homologacion_id=homologacion.id))
		except Exception as err:
			flash(f'Ocurrió un error al intentar guardar los datos. Error: {err}', 'danger')
			return redirect(url_for('homologaciones.add_homologacion'))
	else:
		return render_template('create_homologacion.html', title='Agregar código', 
												form=form, legend="Agregar código homologacion")


@homologaciones.route("/homologacion-<int:homologacion_id>-delete", methods=['GET', 'POST'])
@role_required("Admin", "Comercial")
def delete_homologacion(homologacion_id):
	homologacion = Homologacion.query.get_or_404(homologacion_id)
	db.session.delete(homologacion)
	db.session.commit()
	flash("El código homologacion ha sido eliminado!", 'success')
	return redirect(url_for('homologaciones.all_homologaciones'))