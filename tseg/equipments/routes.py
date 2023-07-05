from flask import render_template, request, Blueprint, flash, redirect, url_for, current_app
from flask_login import current_user, login_required
from tseg.models import Equipment, Client, Historia, Marca, Modelo, Frecuencia, Domicilio, Localidad, Provincia
from tseg.equipments.forms import EquipmentForm
from tseg.users.utils import role_required, identificador_en_corchete, dateFormat, buscarLista
from tseg import db
from datetime import datetime
from sqlalchemy import func


equipments = Blueprint('equipments', __name__)


@equipments.route("/all_equipments")
def all_equipments():	
	all_equips = buscarLista(Equipment)
	orderBy = current_app.config["ORDER_EQUIPOS"]
	image_path = url_for("static", filename='models_pics/')
	return render_template('all_equipments.html',
							lista=all_equips,
							orderBy = orderBy,
							title='Equipos', image_path=image_path)


@equipments.route("/equipment-<int:equipment_id>")
def equipment(equipment_id):
	equipment = Equipment.query.get_or_404(equipment_id)
	historias =  buscarLista(Historia, equipment)
	orderBy = current_app.config['ORDER_HISTORIAS']
	image_path = url_for("static", filename='models_pics/')
	return render_template("equipment.html", title=equipment.modelo_eq.nombre,
											equipment=equipment,
											legend="Ver Equipo",
											orderBy = orderBy,
											lista=historias, 
											image_path=image_path
											)

@equipments.route("/add_equipment-<string:client_id>", methods=['GET','POST'] )
@role_required("Admin", "Técnico")
def add_equipment(client_id):	
	form = EquipmentForm()	
	if form.validate_on_submit():
		client_id = identificador_en_corchete(form.owner.data)
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
		try:
			db.session.add(equipment)
			db.session.commit()
			flash(f'Equipo {equipment.numSerie} agregado!', 'success')
			return redirect(url_for('equipments.equipment', equipment_id=equipment.id, filterBy='date_modified',filterOrder='desc'))
		except Exception as err:
			flash(f'Ocurrió un error al intentar guardar los datos. Error: {err}', 'danger')
			return redirect(url_for('equipments.add_equipment', client_id=client_id))
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
		client_id = identificador_en_corchete(form.owner.data)
		marca = Marca.query.filter_by(nombre=form.marca.data).first()
		modelo = Modelo.query.filter_by(nombre=form.modelo.data).first()
		frecuencia = Frecuencia.query.filter_by(canal=form.frecuencia.data).first()
		equipment.numSerie = form.numSerie.data
		equipment.client_id = client_id
		equipment.marca_id = marca.id
		equipment.modelo_id = modelo.id
		equipment.frecuencia_id = frecuencia.id		
		equipment.content = form.content.data
		equipment.anio = form.anio.data		
		equipment.date_modified = dateFormat()
		try:
			db.session.commit()
			flash(f"Se guardaron los cambios", 'success')
			return redirect(url_for('equipments.equipment', equipment_id=equipment.id, 
														filterBy='date_modified',
														filterSort='desc'))
		except Exception as err:
			flash(f'Ocurrió un error al intentar guardar los datos. Error: {err}', 'danger')
			return redirect(url_for('equipments.update_equipment', equipment_id=equipment.id))
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
	for historia in equipment.historias:
		db.session.delete(historia)
	for orden in equipment.ordenes_reparacion:
		db.session.delete(orden)
	db.session.delete(equipment)
	db.session.commit()
	flash(f"El equipo ha sido eliminado!", 'success')
	return redirect(url_for('equipments.all_equipments', filterBy='anio', filterOrder='desc'))


@equipments.route("/historias_equipo-<int:equipment_id>-<int:tipologia_id>")
def historias_equipo(equipment_id, tipologia_id):
	equipo = Equipment.query.filter_by(id=equipment_id).first_or_404()
	historias = buscarLista(Historia, equipo)	
	orderBy = current_app.config['ORDER_HISTORIAS']	
	return render_template('historias_equipo.html', 
						title=equipo.modelo_eq.nombre, 
						lista=historias,
						orderBy = orderBy,
						equipo=equipo)


@role_required("Admin")
@equipments.route("/reporte_zonal")
def reporte_zona():
	all_equips = Equipment.query.order_by(Equipment.id).join(Client, Equipment.client_id == Client.id).\
    join(Domicilio, Client.domicilio_id == Domicilio.id).\
    join(Localidad, Domicilio.localidad_id == Localidad.id).\
    join(Provincia, Localidad.provincia_id == Provincia.id).\
    where(Provincia.nombre=='Córdoba').all()	
	orderBy = current_app.config["ORDER_EQUIPOS"]
	image_path = url_for("static", filename='models_pics/')
	return render_template('reporte_zona.html',
							lista=all_equips,
							orderBy = orderBy,
							title='Reporte por zona', image_path=image_path)