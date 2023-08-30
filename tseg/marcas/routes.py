from flask import render_template, request, Blueprint, flash, redirect, url_for, current_app
from flask_login import login_required
from tseg.models import Marca, Homologacion
from tseg.marcas.forms import MarcaForm
from tseg.users.utils import role_required, buscarLista, save_picture
from tseg import db
import re

from datetime import datetime


marcas = Blueprint('marcas', __name__)

@marcas.route("/all_marcas")
@login_required
def all_marcas():
	try:
		select_item = request.args.get('selectItem', '')
		if select_item:			
			return redirect(url_for('marcas.marca', marca_id=select_item))
	except Exception as err:
		flash(f'Ocurrió un error al intentar mostrar el Item. Error: {err}', 'danger')
		return redirect(url_for('marcas.all_marcas'))
	all_marcas = buscarLista(Marca)	
	orderBy = current_app.config['ORDER_MARCAS']
	item_type = 'Marca'
	return render_template('all_marcas.html', 
							lista=all_marcas,
							orderBy=orderBy,
							title='Marcas de marcas',							
							item_type=item_type)

@marcas.route("/marca-<int:marca_id>-update", methods=['GET', 'POST'])
@login_required
def marca(marca_id):
	marca = Marca.query.get_or_404(marca_id)	
	form = MarcaForm()
	if form.validate_on_submit():		
		marca.nombre = form.nombre.data		
		try:			
			db.session.commit()
			flash(f"La marca {marca.nombre} ha sido actualizada.", 'success')
			return redirect(url_for('marcas.marca', marca_id=marca.id))
		except Exception as err:
			flash(f'Ocurrió un error al intentar guardar los datos. Error: {err}', 'danger')
			return redirect(url_for('marcas.marca', marca_id=marca.id))
	elif request.method == 'GET':		
		form.nombre.data = marca.nombre
	return render_template('marca.html',
						title='Marca de modelo de equipo',						
						form=form,
						marca=marca)


@marcas.route("/add_marca", methods=['GET','POST'] )
@role_required("Admin", "Comercial")
def add_marca():
	form = MarcaForm()
	if form.validate_on_submit():		
		marca = Marca(nombre=form.nombre.data)
		try:
			db.session.add(marca)
			db.session.commit()
			flash(f'marca "{marca.nombre}" agregada!', 'success')
			return redirect(url_for('marcas.marca', marca_id=marca.id))
		except Exception as err:
			flash(f'Ocurrió un error al intentar guardar los datos. Error: {err}', 'danger')
			return redirect(url_for('marcas.add_marca'))
	return render_template('create_marca.html', title='Agregar marca', 
												form=form, legend="Agregar marca")


@marcas.route("/marca-<int:marca_id>-delete", methods=['GET', 'POST'])
@role_required("Admin", "Comercial")
def delete_marca(marca_id):
	marca = Marca.query.get_or_404(marca_id)
	db.session.delete(marca)
	db.session.commit()
	flash("La marca ha sido eliminada!", 'success')
	return redirect(url_for('marcas.all_marcas'))