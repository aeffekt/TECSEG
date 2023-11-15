from flask import render_template, request, Blueprint, flash, redirect, url_for, current_app
from flask_login import login_required
from tseg.models import Modelo, Client, Historia, Homologacion, Marca
from tseg.modelos.forms import ModeloForm
from tseg.users.utils import role_required, buscarLista, save_picture
from tseg import db
import os

from datetime import datetime


modelos = Blueprint('modelos', __name__)

@modelos.route("/all_modelos")
@login_required
def all_modelos():
	try:
		select_item = request.args.get('selectItem', '')
		if select_item:			
			return redirect(url_for('modelos.modelo', modelo_id=select_item))
	except Exception as err:
		flash(f'Ocurrió un error al intentar mostrar el Item. Error: {err}', 'danger')
		return redirect(url_for('modelos.all_modelos'))
	all_modelos = buscarLista(Modelo)
	image_path = url_for("static", filename='models_pics/')
	orderBy = current_app.config['ORDER_MODELOS']
	item_type = 'Modelo'
	return render_template('all_modelos.html', 
							lista=all_modelos,
							orderBy=orderBy,
							title='Modelos de equipo',
							image_path=image_path,
							item_type=item_type)


@modelos.route("/modelo-<int:modelo_id>-update", methods=['GET', 'POST'])
@login_required
def modelo(modelo_id):
	modelo = Modelo.query.get_or_404(modelo_id)	
	form = ModeloForm(modelo)
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data, 'models_pics', str(modelo))
			modelo.image_file = picture_file		
		modelo.marca_id = form.marca.data
		modelo.nombre = form.nombre.data
		modelo.anio = form.anio.data
		modelo.tipo_modelo_id = form.tipo_modelo.data
		modelo.descripcion = form.descripcion.data
		now = datetime.now()
		now = now.strftime("%Y-%m-%dT%H:%M:%S")
		try:
			modelo.date_modified = datetime.fromisoformat(now)
			db.session.commit()
			flash(f"El modelo {modelo.nombre} ha sido actualizado.", 'success')
			return redirect(url_for('modelos.modelo', modelo_id=modelo.id))
		except Exception as err:
			flash(f'Ocurrió un error al intentar guardar los datos. Error: {err}', 'danger')
			return redirect(url_for('modelos.modelo', modelo_id=modelo.id))	
	form.anio.default = modelo.anio
	form.tipo_modelo.default=modelo.tipo_modelo.id
	form.process()
	form.marca.data = modelo.marca.id	
	form.nombre.data = modelo.nombre	
	form.descripcion.data = modelo.descripcion
	image_path = url_for("static", filename='models_pics/')	
	return render_template('modelo.html',
						title='Modelo de equipo',						
						image_path=image_path,
						form=form,
						modelo=modelo)


@modelos.route("/add_modelo", methods=['GET','POST'] )
@role_required("Admin", "Comercial")
def add_modelo():
	form = ModeloForm()
	if form.validate_on_submit():	
		homologacion = Homologacion.query.filter_by(modelo=form.nombre.data).first()
		modelo = Modelo(nombre=form.nombre.data,
						anio=form.anio.data,
						descripcion=form.descripcion.data,
						tipo_modelo_id=form.tipo_modelo.data,
						homologacion=homologacion,
						marca_id=form.marca.data)
		if form.picture.data:
			picture_file = save_picture(form.picture.data, 'models_pics', str(modelo))
			modelo.image_file = picture_file			
		try:
			db.session.add(modelo)
			db.session.commit()
			flash(f'modelo {modelo.nombre} agregado!', 'success')
			return redirect(url_for('modelos.modelo', modelo_id=modelo.id))
		except Exception as err:
			flash(f'Ocurrió un error al intentar guardar los datos. Error: {err}', 'danger')
			return redirect(url_for('modelos.add_modelo'))
	return render_template('create_modelo.html', title='Agregar modelo', 
												form=form, legend="Agregar modelo")


@modelos.route("/modelo-<int:modelo_id>-delete", methods=['GET', 'POST'])
@role_required("Admin", "Comercial")
def delete_modelo(modelo_id):
	modelo = Modelo.query.get_or_404(modelo_id)
	try:		
		db.session.delete(modelo)
		db.session.commit()
		picture_path = os.path.join(current_app.root_path, f'static\\models_pics', modelo.image_file)		
		if os.path.exists(picture_path) and modelo.image_file != "default_eq.png":
			os.remove(picture_path)			
		flash("El modelo ha sido eliminado!", 'success')
		return redirect(url_for('modelos.all_modelos'))
	except Exception as e:
		db.session.rollback() 
		flash("Ocurrió un error al intentar eliminar: Es probable que el modelo se encuentre asignado a un equipo.", 'warning')
		flash(f"Detalles del error: {e}", 'danger')
		return redirect(url_for('modelos.modelo', modelo_id=modelo.id))	