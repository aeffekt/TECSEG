from flask import render_template, request, Blueprint, flash, redirect, url_for, current_app
from flask_login import current_user, login_required
from tseg.models import Equipment, Client, Eq_detail
from tseg.equipments.forms import EquipmentForm
from tseg.users.forms import SearchForm
from tseg.users.utils import role_required, extraerId, dateFormat

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
	page = request.args.get('page', 1, type=int) # num pagina de mensajes
	all_equips = Equipment.query.order_by(Equipment.date_modified.desc()).paginate(page=page, per_page=current_app.config['PER_PAGE'])
	return render_template('all_equipments.html', 
							all_equipments=all_equips, 
							title='Equipos')


'''  Ordenamiento de ALL_EQUIPMENTS... a mejorar!
@equipments.route("/all_equipments")
def all_equipments():
	sort_by = request.args.get('sort-by')
	sort_order = request.args.get('sort-order')

	page = request.args.get('page', 1, type=int)
	per_page = current_app.config['PER_PAGE']

	query = Equipment.query

	# Ordenar por sort_by
	if sort_by == 'date_created':
		order_by_column = Equipment.date_created
	elif sort_by == 'anio':
		order_by_column = Equipment.anio		
	elif sort_by == 'title':
		order_by_column = Equipment.title		
	else:
		order_by_column = Equipment.date_modified		

	# Orden ascendente o descendente
	if sort_order == 'asc':		
		query = query.order_by(order_by_column.asc())		
	else:		
		query = query.order_by(order_by_column.desc())		
	
	all_equips = query.paginate(page=page, per_page=per_page)
	return render_template('all_equipments.html', 
							all_equipments=all_equips, 
							title='Equipos',
							sort_by=sort_by, 
							sort_order=sort_order)
'''

@equipments.route("/equipment-<int:equipment_id>")
def equipment(equipment_id):
	equipment = Equipment.query.get_or_404(equipment_id)
	page = request.args.get('page', 1, type=int) # num pagina de mensajes
	historias =  Eq_detail.query.filter_by(equipo_historia=equipment)\
					.order_by(Eq_detail.date_modified.desc())\
					.paginate(page=page, per_page=10)
	return render_template("equipment.html", title=equipment.title,
											equipment=equipment,
											legend="Ver Equipo",
											historias=historias)

@equipments.route("/add_equipment-<string:client_id>", methods=['GET','POST'] )
@role_required("Admin", "Técnico")
def add_equipment(client_id):	
	form = EquipmentForm()	
	client = Client.query.filter_by(id=client_id).first()
	if form.validate_on_submit():		
		equipment = Equipment(title=form.title.data, 
							numSerie=form.numSerie.data, 
							content=form.content.data, 
							anio=form.anio.data, 
							author_eq=current_user, 
							client_id=client_id)
		db.session.add(equipment)
		db.session.commit()
		flash(f'Equipo {equipment.title} agregado!', 'success')
		return redirect(url_for('equipments.equipment', equipment_id=equipment.id))	
	form.owner.default = f'[{client.id}] {client.client_name}, {client.business_name}'	
	form.process()
	return render_template('create_equipment.html', title='Agregar equipo', 
												form=form, legend="Agregar equipo")


@equipments.route("/equipment-<int:equipment_id>-update", methods=['GET', 'POST'])
@role_required("Admin", "Técnico")
def update_equipment(equipment_id):
	equipment = Equipment.query.get_or_404(equipment_id)
	form = EquipmentForm()
	if form.validate_on_submit():		
		client_id = extraerId(form.owner.data)
		equipment.client_id = client_id
		equipment.title = form.title.data
		equipment.numSerie = form.numSerie.data		
		equipment.content = form.content.data
		equipment.anio = form.anio.data		
		equipment.date_modified = dateFormat()
		db.session.commit()
		flash(f"Se guardaron los cambios", 'success')
		return redirect(url_for('equipments.equipment', equipment_id=equipment.id))
	elif request.method == 'GET':		
		form.owner.default = f'[{equipment.owner.id}] {equipment.owner.client_name}, {equipment.owner.business_name}'		
		form.anio.default = equipment.anio
		form.process()
		form.title.data = equipment.title
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
	page = request.args.get('page', 1, type=int) # num pagina de mensajes
	historias =  Eq_detail.query.filter_by(tipologia_id=tipologia_id, equipment_id=equipment_id)\
					.order_by(Eq_detail.date_modified.desc())\
					.paginate(page=page, per_page=10)	
	return render_template('historias_equipo.html', title=equipo.title, historias=historias, equipo=equipo)