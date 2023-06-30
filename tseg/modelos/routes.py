from flask import render_template, request, Blueprint, flash, redirect, url_for, current_app
from flask_login import login_required
from tseg.models import Modelo, Client, Historia
from tseg.modelos.forms import ModeloForm
from tseg.users.forms import SearchForm
from tseg.users.utils import role_required, buscarLista, save_picture
from tseg import db
import re

from datetime import datetime


modelos = Blueprint('modelos', __name__)

# pass stuff to navbar through layout (used to search)
@modelos.context_processor
def layout():
	form = SearchForm()
	return dict(form=form)


@modelos.route("/all_modelos")
def all_modelos():
	all_modelos = buscarLista(Modelo)
	image_path = url_for("static", filename='models_pics/')
	filtrar_por = current_app.config['FILTROS_MODELOS']
	return render_template('all_modelos.html', 
							lista=all_modelos,
							filtrar_por=filtrar_por,
							title='Modelos de equipo',
							image_path=image_path)

@modelos.route("/modelos-<int:modelo_id>", methods=['GET', 'POST'])
@login_required
def modelo(modelo_id):
	modelo = Modelo.query.get_or_404(modelo_id)
	form = ModeloForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data, 'models_pics')
			modelo.image_file = picture_file
		modelo.nombre = form.nombre.data
		modelo.descripcion = form.descripcion.data		
		db.session.commit()
		flash(f"La cuenta {modelo.nombre} ha sido actualizada.", 'success')
		return redirect(url_for('modelos.modelo', modelo_id=modelo.id))
	elif request.method == 'GET':		
		form.nombre.data = modelo.nombre
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
		modelo = Modelo(nombre=form.nombre.data, 
							descripcion=form.descripcion.data)
		db.session.add(modelo)
		db.session.commit()
		flash(f'modelo {modelo.nombre} agregado!', 'success')
		return redirect(url_for('modelos.modelo', modelo_id=modelo.id))
	return render_template('create_modelo.html', title='Agregar modelo', 
												form=form, legend="Agregar modelo")


@modelos.route("/modelo-<int:modelo_id>-update", methods=['GET', 'POST'])
@role_required("Admin", "Técnico")
def update_modelo(modelo_id):
	modelo = Modelo.query.get_or_404(modelo_id)
	form = ModeloForm()
	if form.validate_on_submit():		
		modelo.nombre = form.nombre.data
		modelo.descripcion = form.descripcion.data		
		now = datetime.now()
		now = now.strftime("%Y-%m-%dT%H:%M:%S")
		modelo.date_modified = datetime.fromisoformat(now)
		db.session.commit()
		flash("El modelo ha sido editado con éxito", 'success')
		return redirect(url_for('modelos.modelo', modelo_id=modelo.id))
	elif request.method == 'GET':		
		form.nombre.data = modelo.nombre
		form.descripcion.data = modelo.descripcion		
	return render_template('create_modelo.html',title='Editar modelo', 
												form=form,
												legend="Editar modelo")

@modelos.route("/modelo-<int:modelo_id>-delete", methods=['POST'])
@role_required("Admin", "Técnico")
def delete_modelo(modelo_id):
	modelo = Modelo.query.get_or_404(modelo_id)
	db.session.delete(modelo)
	db.session.commit()
	flash("El modelo ha sido eliminado!", 'success')
	return redirect(url_for('modelos.all_modelos'))