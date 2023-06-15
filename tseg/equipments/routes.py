from flask import render_template, request, Blueprint, flash, redirect, url_for, current_app
from flask_login import current_user, login_required
from tseg.models import Equipment, Client, Eq_detail
from tseg.equipments.forms import EquipmentForm
from tseg.users.forms import SearchForm
from tseg.users.utils import role_required, extraerId
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
	all_equips = Equipment.query.order_by(Equipment.date_created.desc()).paginate(page=page, per_page=current_app.config['PER_PAGE'])
	return render_template('all_equipments.html', 
							all_equipments=all_equips, 
							title='Equipos')


@equipments.route("/equipment-<int:equipment_id>")
def equipment(equipment_id):
	equipment = Equipment.query.get_or_404(equipment_id)
	page = request.args.get('page', 1, type=int) # num pagina de mensajes
	historias =  Eq_detail.query.filter_by(equipo=equipment)\
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
	if form.validate_on_submit():
		client_id = extraerId(form.owner.data)		
		equipment = Equipment(title=form.title.data, 
							numSerie=form.numSerie.data, 
							content=form.content.data, 
							author_eq=current_user, 
							client_id=client_id)
		db.session.add(equipment)
		db.session.commit()
		flash(f'Equipo {equipment.title} agregado!', 'success')
		return redirect(url_for('equipments.equipment', equipment_id=equipment.id))	
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



		# !!!!!!!!! agregar modificador!! y dejar autor sin cambiar
		equipment.author_eq = current_user
		now = datetime.now()
		now = now.strftime("%Y-%m-%dT%H:%M:%S")
		equipment.date_modified = datetime.fromisoformat(now)
		db.session.commit()
		flash("El equipo ha sido editado con éxito", 'success')
		return redirect(url_for('equipments.equipment', equipment_id=equipment.id))
	elif request.method == 'GET':		
		form.owner.default = f'[{equipment.owner.id}] {equipment.owner.client_name}, {equipment.owner.business_name}'
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