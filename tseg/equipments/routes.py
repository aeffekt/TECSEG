from flask import render_template, request, Blueprint, flash, redirect, url_for, current_app
from flask_login import current_user, login_required
from tseg.models import Equipment, Client, Historia, Marca, Modelo, Frecuencia
from tseg.equipments.forms import EquipmentForm
from tseg.users.forms import SearchForm
from tseg.users.utils import role_required, extraerId, dateFormat, buscarLista
from tseg import db
from datetime import datetime


equipments = Blueprint('equipments', __name__)

# pass stuff to navbar through layout (used to search)
@equipments.context_processor
def layout():
	form = SearchForm()
	return dict(form=form)


@equipments.route("/all_equipments")
def all_equipments():
	all_equips = buscarLista(Equipment)
	filtrar_por = current_app.config["FILTROS_EQUIPOS"]

	return render_template('all_equipments.html',
							lista=all_equips,
							filtrar_por = filtrar_por,
							title='Equipos')


@equipments.route("/equipment-<int:equipment_id>")
def equipment(equipment_id):
	equipment = Equipment.query.get_or_404(equipment_id)
	historias =  buscarLista(Historia, equipment)
	filtrar_por = current_app.config['FILTROS_HISTORIAS']
	return render_template("equipment.html", title=equipment.modelo_eq.nombre,
											equipment=equipment,
											legend="Ver Equipo",
											filtrar_por = filtrar_por,
											lista=historias
											)

@equipments.route("/add_equipment-<string:client_id>", methods=['GET','POST'] )
@role_required("Admin", "Técnico")
def add_equipment(client_id):	
	form = EquipmentForm()	
	if form.validate_on_submit():
		client_id = extraerId(form.owner.data)
		marca = Marca.query.filter_by(nombre=form.marca.data).first()
		modelo = Modelo.query.filter_by(nombre=form.modelo.data).first()
		frecuencia = Frecuencia.query.filter_by(canal=form.frecuencia.data).first()
		equipment = Equipment(numSerie=form.numSerie.data,
							content=form.content.data,
							anio=form.anio.data,
							author_eq=current_user,
							marca_eq=marca,
							modelo_eq=modelo,
							frecuencia_eq=frecuencia,
							client_id=client_id)
		db.session.add(equipment)
		db.session.commit()
		flash(f'Equipo {equipment.modelo_eq.nombre} agregado!', 'success')
		return redirect(url_for('equipments.equipment', equipment_id=equipment.id))	
	client = Client.query.filter_by(id=client_id).first()
	if client:
		form.owner.default = f'[{client.id}] {client.nombre} {client.apellido}, {client.business_name}'
		form.process()
	return render_template('create_equipment.html', title='Agregar equipo', 
												form=form, 
												legend="Agregar equipo")


@equipments.route("/equipment-<int:equipment_id>-update", methods=['GET', 'POST'])
@role_required("Admin", "Técnico")
def update_equipment(equipment_id):
	equipment = Equipment.query.get_or_404(equipment_id)
	form = EquipmentForm()
	if form.validate_on_submit():		
		client_id = extraerId(form.owner.data)
		marca = Marca.query.filter_by(nombre=form.marca.data).first()
		modelo = Modelo.query.filter_by(nombre=form.modelo.data).first()
		frecuencia = Frecuencia.query.filter_by(canal=form.frecuencia.data).first()
		equipment.client_id = client_id
		equipment.marca_id = marca.id
		equipment.modelo_id = modelo.id
		equipment.frecuencia_id = frecuencia.id
		equipment.numSerie = form.numSerie.data
		equipment.content = form.content.data
		equipment.anio = form.anio.data		
		equipment.date_modified = dateFormat()
		db.session.commit()
		flash(f"Se guardaron los cambios", 'success')
		return redirect(url_for('equipments.equipment', equipment_id=equipment.id, 
														filterBy='date_modified',
														filterSort='desc'))
	elif request.method == 'GET':		
		form.owner.default = f'[{equipment.owner.id}] {equipment.owner.nombre} {equipment.owner.apellido}, {equipment.owner.business_name}'
		form.anio.default = equipment.anio
		form.process()
		form.marca.data = equipment.marca_eq.nombre if equipment.marca_eq else None
		form.modelo.data = equipment.modelo_eq.nombre if equipment.modelo_eq else None
		form.frecuencia.data = equipment.frecuencia_eq.canal if equipment.frecuencia_eq else None
		form.numSerie.data = equipment.numSerie
		form.content.data = equipment.content		
	return render_template('create_equipment.html',title='Editar equipo', 
												form=form,
												legend="Editar equipo")

@equipments.route("/equipment-<int:equipment_id>-delete", methods=['POST'])
@role_required("Admin", "Técnico")
def delete_equipment(equipment_id):
	equipment = Equipment.query.get_or_404(equipment_id)
	db.session.delete(equipment)
	db.session.commit()
	flash("El equipo ha sido eliminado!", 'success')
	return redirect(url_for('equipments.all_equipments'))


@equipments.route("/historias_equipo-<int:equipment_id>-<int:tipologia_id>")
def historias_equipo(equipment_id, tipologia_id):	
	equipo = Equipment.query.filter_by(id=equipment_id).first_or_404()
	historias = buscarLista(Historia, equipo)	
	filtrar_por = current_app.config['FILTROS_HISTORIAS']
	return render_template('historias_equipo.html', 
						title=equipo.modelo_eq.nombre, 
						lista=historias,
						filtrar_por = filtrar_por,
						equipo=equipo)