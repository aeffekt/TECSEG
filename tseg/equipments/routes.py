from flask import render_template, request, Blueprint, flash, redirect, url_for, current_app
from flask_login import current_user, login_required
from tseg.models import Equipment, Client, Historia, Modelo, Frecuencia, Orden_reparacion
from tseg.equipments.forms import EquipmentForm
from tseg.users.utils import role_required, identificador_en_corchete, dateFormat, buscarLista
from tseg import db
from datetime import datetime
from sqlalchemy import func
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


equipments = Blueprint('equipments', __name__)

@login_required
@equipments.route("/all_equipments")
def all_equipments():
	image_path = url_for("static", filename='models_pics/')
	select_item = request.args.get('selectItem', '')
	if select_item:
		numSerie = identificador_en_corchete(select_item)
		equipment = Equipment.query.filter_by(numSerie=numSerie).first()		
		return redirect(url_for('equipments.equipment', equipment_id=equipment.id, 
														filterBy='date_modified',
														filterSort='desc'))		
	all_equips = buscarLista(Equipment)
	orderBy = current_app.config["ORDER_EQUIPOS"]
	item_type = 'Equipo'
	return render_template('all_equipments.html',
							lista=all_equips,
							orderBy = orderBy,
							title='Equipos', 
							image_path=image_path,
							item_type=item_type)


@login_required
@equipments.route("/equipment-<int:equipment_id>")
def equipment(equipment_id):	
	select_item = request.args.get('selectItem')
	if select_item:
		historia_id = identificador_en_corchete(select_item)		
		return redirect(url_for('historias.historia', historia_id=historia_id))
	equipment = Equipment.query.get_or_404(equipment_id)
	historias =  buscarLista(Historia, equipment)
	reparaciones = buscarLista(Orden_reparacion, equipment)
	orderBy = current_app.config['ORDER_HISTORIAS']	
	image_path = url_for("static", filename='models_pics/')
	# texto para toolbar
	item_type="Historia"	
	path_etiqueta = url_for("static", filename='pdfs/')	
	return render_template("equipment.html", title=equipment.modelo,
											equipment=equipment,
											legend="Ver Equipo",
											orderBy = orderBy,
											lista=historias,
											reparaciones=reparaciones,
											image_path=image_path,
											item_type=item_type,
											path_etiqueta=path_etiqueta
											)

@equipments.route("/add_equipment-<string:client_id>", methods=['GET','POST'] )
@role_required("Admin", "Técnico")
def add_equipment(client_id):	
	form = EquipmentForm()
	try:		
		if form.validate_on_submit():		
			client_id = identificador_en_corchete(form.owner.data)		
			nombre_mod, anio_mod = form.modelo.data.split()
			modelo = Modelo.query.filter_by(nombre=nombre_mod, anio=anio_mod).first()
			frecuencia = Frecuencia.query.filter_by(canal=form.frecuencia.data).first()		
			equipment = Equipment(numSerie=form.numSerie.data,
							content=form.content.data,
							anio=form.anio.data,
							author_eq=current_user,
							modelo=modelo,
							frecuencia_eq=frecuencia,
							client_id=client_id)
		
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
		nombre_mod, anio_mod = form.modelo.data.split()
		modelo = Modelo.query.filter_by(nombre=nombre_mod, anio=anio_mod).first()
		frecuencia = Frecuencia.query.filter_by(canal=form.frecuencia.data).first()
		equipment.numSerie = form.numSerie.data
		equipment.client_id = client_id
		equipment.modelo = modelo
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
		form.modelo.default = equipment.modelo if equipment.modelo else None
		form.frecuencia.default = equipment.frecuencia_eq.canal if equipment.frecuencia_eq else None		
		form.process()		
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


@login_required
@equipments.route("/historias_equipo-<int:equipment_id>-<int:tipologia_id>")
def historias_equipo(equipment_id, tipologia_id):
	select_item = request.args.get('selectItem', '')	
	if select_item:
		historia_id = identificador_en_corchete(select_item)
		return redirect(url_for('historias.historia', historia_id=historia_id))
	equipo = Equipment.query.filter_by(id=equipment_id).first_or_404()
	historias = buscarLista(Historia, equipo)
	if tipologia_id:
		historias = historias.filter_by(tipologia_id=tipologia_id)
	orderBy = current_app.config['ORDER_HISTORIAS']	
	return render_template('historias_equipo.html', 
						title=equipo.modelo.nombre, 
						lista=historias,
						orderBy = orderBy,
						equipo=equipo)


@equipments.route("/print_etiqueta-<int:equipment_id>")
@login_required
def print_etiqueta(equipment_id):    
	try:
		# datos del equipo
		equipo = Equipment.query.get_or_404(equipment_id)		
		modelo = equipo.modelo.nombre
		numSerie = equipo.numSerie
		homologacion = equipo.modelo.homologacion
		
		# formateo del texto
		heading = f'Etiqueta de equipo'
		numSerie_string = str(equipo.numSerie).replace('/', '_')		
		name_etiqueta = f"{numSerie_string}.pdf"		
		path_etiqueta = f'tseg/static/pdfs/{name_etiqueta}'
		
		# config CANVAS
		x, y = A4
		hoja_A4 = canvas.Canvas(path_etiqueta, pagesize=A4)
		font_size = 9  # Tamaño de fuente en puntos
		hoja_A4.setFont("Helvetica", font_size)  # Establecer el tamaño de fuente en el lienzo        
		hoja_A4.setLineWidth(0.5)

		# texto de la etiqueta
		hoja_A4.drawCentredString(100, y-50, heading)
		hoja_A4.drawCentredString(35, y-65, 'Modelo')
		hoja_A4.drawCentredString(100, y-65, modelo)
		hoja_A4.drawCentredString(35, y-80, 'numSerie')
		hoja_A4.drawCentredString(100, y-80, numSerie)
		if homologacion:
			hoja_A4.drawCentredString(35, y-95, 'homologacion')
			hoja_A4.drawCentredString(100, y-95, homologacion.codigo)

		# dibujos de etiqueta		
		hoja_A4.rect(65, y-55, 70, -44) #  X, Y, DeltaX, DeltaY
		hoja_A4.line(65, y-70, 135, y-70)
		hoja_A4.line(65, y-85, 135, y-85)

		# guardar datos
		hoja_A4.save()
		equipo.etiqueta_file = name_etiqueta
		db.session.commit()

		flash(f"La etiqueta se generó correctamente. ",'success')
	except Exception as err:
		flash(f"Ocurrió un error al generar la etiqueta: {err}",'warning')
	finally:
		return redirect(url_for('equipments.equipment', equipment_id=equipo.id, filterBy='date_modified',filterOrder='desc'))