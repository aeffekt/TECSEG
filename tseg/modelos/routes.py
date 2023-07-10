from flask import render_template, request, Blueprint, flash, redirect, url_for, current_app
from flask_login import login_required
from tseg.models import Modelo, Client, Historia, Homologacion, Marca
from tseg.modelos.forms import ModeloForm
from tseg.users.utils import role_required, buscarLista, save_picture
from tseg import db
import re

from datetime import datetime


modelos = Blueprint('modelos', __name__)

@modelos.route("/all_modelos")
def all_modelos():
	try:
		select_item = request.args.get('selectItem', '')
		if select_item:
			nombre_modelo, anio = select_item.split()
			# divide el __repr__ y obtiene el código en pos 2		
			modelo = Modelo.query.filter_by(nombre=nombre_modelo, anio=anio).first()
			return redirect(url_for('modelos.modelo', modelo_id=modelo.id))
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
	form = ModeloForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data, 'models_pics')
			modelo.image_file = picture_file		
		marca = Marca.query.filter_by(nombre=form.marca.data).first()
		modelo.marca = marca
		modelo.nombre = form.nombre.data
		modelo.anio = form.anio.data
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
	elif request.method == 'GET':
		form.marca.data = modelo.marca.nombre if modelo.marca else None	
		form.nombre.data = modelo.nombre
		form.anio.data = modelo.anio
		form.descripcion.data = modelo.descripcion	
		image_file = url_for("static", filename='models_pics/'+modelo.image_file)
	return render_template('modelo.html',
						title='Modelo de equipo', 
						image_file=image_file,
						form=form,
						modelo=modelo)


@modelos.route("/add_modelo", methods=['GET','POST'] )
@role_required("Admin", "Técnico")
def add_modelo():
	form = ModeloForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data, 'models_pics')			
		homologacion = Homologacion.query.filter_by(modelo=form.nombre.data).first()
		marca = Marca.query.filter_by(nombre=form.marca.data).first()
		modelo = Modelo(nombre=form.nombre.data,
						anio=form.anio.data,
						descripcion=form.descripcion.data,
						homologacion=homologacion,						
						marca=marca,						
						image_file=picture_file)
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
@role_required("Admin", "Técnico")
def delete_modelo(modelo_id):
	modelo = Modelo.query.get_or_404(modelo_id)
	db.session.delete(modelo)
	db.session.commit()
	flash("El modelo ha sido eliminado!", 'success')
	return redirect(url_for('modelos.all_modelos'))