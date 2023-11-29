from flask import render_template, request, Blueprint, flash, redirect, url_for, current_app, jsonify
from flask_login import current_user, login_required
from tseg.models import Equipment, Historia, Orden_reparacion, Frecuencia, Detalle_trabajo, Orden_trabajo, dateFormat
from tseg.equipments.forms import EquipmentForm
from tseg.users.utils import role_required, buscarLista, error_logger
from tseg.equipments.utils import (print_caratula_pdf, print_etiqueta_pdf, upload_files, get_full_folder_path, 
								   get_files_info, get_folder_path, delete_file)
from tseg import db
import os, shutil # shutil se usa para borrar un directorio mas archivos


equipments = Blueprint('equipments', __name__)


# Busca los sistemas de todos los equipos de la misma OT
@equipments.route('/get_sistemas', methods=['GET', 'POST'])
def get_sistemas():
	detalle_trabajo_id = request.args.get('detalle_trabajo')	
	sistemas=[]
	dt = Detalle_trabajo.query.get_or_404(detalle_trabajo_id)
	ot = Orden_trabajo.query.get(dt.orden_trabajo.id)	
	for detalle in ot.detalles_trabajo:
		for equipo in detalle.equipments:
			if equipo.sistema not in sistemas:
				sistemas.append(equipo.sistema)	
	return jsonify(sistemas)


@login_required
@equipments.route("/all_equipments")
def all_equipments():
	image_path = url_for("static", filename='models_pics/')
	select_item = request.args.get('selectItem', '')
	if select_item:
		return redirect(url_for('equipments.equipment', equipment_id=select_item, 
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
		return redirect(url_for('historias.historia', historia_id=select_item))
	equipment = Equipment.query.get_or_404(equipment_id)	
	historias =  buscarLista(Historia, equipment)
	reparaciones = buscarLista(Orden_reparacion, equipment, toFilter=False)
	orderBy = current_app.config['ORDER_HISTORIAS']	
	image_path = url_for("static", filename='models_pics/')
	#info de los archivos del equipo
	full_folder_path = get_full_folder_path(equipment)
	archivos_info = get_files_info(full_folder_path)
	folder_path = get_folder_path(equipment)
	# texto para toolbar
	item_type="Historia"
	path_pdfs = url_for("static", filename='pdfs/')	
	return render_template("equipment.html", title=equipment,
											equipment=equipment,
											legend="Ver Equipo",
											orderBy = orderBy,
											lista=historias,
											reparaciones=reparaciones,											
											image_path=image_path,
											item_type=item_type,
											folder_path=folder_path,
											archivos_info=archivos_info,
											path=path_pdfs
											)


@equipments.route("/add_equipment-<string:detalle_trabajo_id>", methods=['GET','POST'] )
@role_required("Admin", "Técnico")
def add_equipment(detalle_trabajo_id):	
	form = EquipmentForm()
	if form.validate_on_submit():
		try:		
			equipment = Equipment(numSerie=form.numSerie.data,
							content=form.content.data,
							anio=form.anio.data,
							author_eq=current_user,
							modelo_id=form.modelo.data,							
							sistema=form.sistema.data,
							detalle_trabajo_id=form.detalle_trabajo.data)		
			db.session.add(equipment)
			for frecuencia_id in form.frecuencias.data:
				frecuencia = Frecuencia.query.get(frecuencia_id)
				if frecuencia:
					equipment.frecuencias.append(frecuencia)
			db.session.commit()
			if form.upload_files.data:
				archivos_seleccionados = request.files.getlist('upload_files')
				if archivos_seleccionados:
					upload_files(archivos_seleccionados, equipment)
			flash(f'Equipo {equipment.numSerie} agregado!', 'success')
			return redirect(url_for('ordenes_trabajo.orden_trabajo', orden_trabajo_id=equipment.detalle_trabajo.orden_trabajo.id))
		except Exception as e:
			error_logger(e)		
			return redirect(url_for('equipments.add_equipment', detalle_trabajo_id=detalle_trabajo_id))	
	form.detalle_trabajo.default = detalle_trabajo_id
	form.process()
	return render_template('create_equipment.html', title='Registrar equipo', 
												form=form, 
												legend="Registrar equipo")


@equipments.route("/equipment-<int:equipment_id>-update", methods=['GET', 'POST'])
@role_required("Admin", "Técnico")
def update_equipment(equipment_id):
	equipment = Equipment.query.get_or_404(equipment_id)
	form = EquipmentForm(equipment)
	if form.validate_on_submit():		
		try:			
			# actualiza las frecuencias del equipo			
			for frecuencia_old in equipment.frecuencias:				
				equipment.frecuencias.remove(frecuencia_old)
			for frecuencia_selected in form.frecuencias.data:
				frecuencia_new = Frecuencia.query.get(frecuencia_selected)
				if frecuencia_new:
					equipment.frecuencias.append(frecuencia_new)
			equipment.numSerie = form.numSerie.data
			equipment.detalle_trabajo_id = form.detalle_trabajo.data
			equipment.modelo_id = form.modelo.data			
			equipment.sistema = form.sistema.data			
			equipment.content = form.content.data
			equipment.anio = form.anio.data
			equipment.date_modified = dateFormat()	
			archivos_seleccionados = request.files.getlist('upload_files')
			if archivos_seleccionados[0].filename!='':
				upload_files(archivos_seleccionados, equipment)
			db.session.commit()
			flash(f"Se guardaron los cambios", 'success')
			return redirect(url_for('equipments.equipment', equipment_id=equipment.id, 
														filterBy='date_modified',
														filterSort='desc'))
		except Exception as e:
			error_logger(e)
			return redirect(url_for('equipments.update_equipment', equipment_id=equipment.id))
	elif request.method == 'GET':
		form.anio.default = equipment.anio
		form.detalle_trabajo.default = equipment.detalle_trabajo.id
		form.modelo.default = equipment.modelo_id
		form.frecuencias.default = [f.id for f in equipment.frecuencias]
		form.sistema.default = equipment.sistema
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
	detalle_trabajo_id = equipment.detalle_trabajo.id
	folder_path = get_full_folder_path(equipment)
	try:
		shutil.rmtree(folder_path)
		flash(f"Los archivos del equipo han sido eliminado!", 'success')
	except Exception as e:
		flash(f"Ocurrió un error al intentar eliminar los archivos del equipo", 'warning')
	try:
		# elimina las historias del equipo
		for historia in equipment.historias:
			db.session.delete(historia)
		# elimina las O.R. del equipo
		for orden in equipment.ordenes_reparacion:
			db.session.delete(orden)
		# elimina las las referencias de frecuencias del equipo
		for frecuencia in equipment.frecuencias:
			equipment.frecuencias.remove(frecuencia)
		db.session.delete(equipment)
		db.session.commit()
		# elimina los archivos del equipo		
		flash(f"El equipo ha sido eliminado!", 'success')		
	except Exception as e:
		error_logger(e)		
	finally:
		return redirect(url_for('detalles_trabajo.detalle_trabajo', detalle_trabajo_id=detalle_trabajo_id))


@login_required
@equipments.route("/historias_equipo-<int:equipment_id>-<int:tipo_historia_id>")
def historias_equipo(equipment_id, tipo_historia_id):
	select_item = request.args.get('selectItem', '')
	if select_item:		
		return redirect(url_for('historias.historia', historia_id=select_item))
	equipo = Equipment.query.filter_by(id=equipment_id).first_or_404()
	historias = buscarLista(Historia, equipo)
	if tipo_historia_id:
		historias = historias.filter_by(tipo_historia_id=tipo_historia_id)
	orderBy = current_app.config['ORDER_HISTORIAS']	
	return render_template('historias_equipo.html', 
						title=equipo.modelo.nombre, 
						lista=historias,
						orderBy = orderBy,
						equipo=equipo)


@equipments.route("/print_pdfs-<int:equipment_id>")
@login_required
def print_pdfs(equipment_id):	
	path = os.path.join(current_app.root_path, 'static/pdfs/')
	equipo = Equipment.query.get_or_404(equipment_id)	
	print_etiqueta_pdf(path, equipo)
	print_caratula_pdf(path, equipo)
	return redirect(url_for('equipments.equipment', equipment_id=equipo.id, filterBy='date_modified',filterOrder='desc'))


# Eliminar archivo del equipo del servidor 
@equipments.route('/delete-file/<path:file_path>/<string:file_name>/<int:equipment_id>', methods=['POST'])
def delete_file_route(file_path, file_name, equipment_id):
	delete_file(file_path, file_name)
	return redirect(url_for('equipments.equipment', equipment_id=equipment_id, filterBy='date_modified',filterOrder='desc'))
