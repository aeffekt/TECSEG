# reportes routes
from flask import render_template, Blueprint, current_app, flash
from flask_login import current_user
from tseg import db
from tseg.models import Orden_reparacion, Equipment, Role, User, Provincia, Domicilio, Localidad, Client, Estado_or, Modelo
from sqlalchemy import func
from tseg.users.utils import role_required
import json


reportes = Blueprint('reportes', __name__)


@reportes.route("/reporte_tecnico")
@role_required("Admin", "ServicioCliente")
def reporte_tecnico():
	query = db.session.query(
				User.username.label('Técnico'),
				func.count(Orden_reparacion.id).label('Pendientes'))\
				.join(Role, User.role_id == Role.id)\
				.filter(Role.role_name == 'tecnico')\
				.join(Orden_reparacion, Orden_reparacion.tecnico_id == User.id)\
				.join(Estado_or, Estado_or.id == Orden_reparacion.estado_id)\
				.filter(Estado_or.descripcion=="Asignada")\
				.group_by(User.username)\
				.order_by(func.count(Orden_reparacion.id).desc())

	# Obtener los resultados
	result = query.all()

	# Obtener los resultados
	asignaciones_tecnicos = query.all()
	orderBy = current_app.config["ORDER_TECNICO"]	
	tecnicos = [item.Técnico for item in asignaciones_tecnicos]
	cantidades = [item.Pendientes for item in asignaciones_tecnicos]
	labels_json = json.dumps(tecnicos)
	cantidades_json = json.dumps(cantidades)

	return render_template('reporte.html',
							chart_type='bar',
							labels=labels_json,
							data=cantidades_json,
							datos_sql=asignaciones_tecnicos,
							orderBy = orderBy,
							nombre_reporte='Reporte de O.R. por técnico',
							title='Reporte técnicos')


@reportes.route("/reporte_zonal")
@role_required("Admin")
def reporte_zona():
	query = db.session.query(
					    Provincia.nombre.label('Provincia'),
					    func.count(Equipment.id).label('Cantidad')
							).\
						join(Localidad, Provincia.localidades).\
						join(Domicilio, Localidad.domicilios).\
						join(Client, Domicilio.clientes).\
						join(Equipment, Client.equipments).\
						group_by(Provincia.nombre).\
						order_by(func.count(Equipment.id).desc())

	# Obtener los resultados
	equipos_por_provincia = query.all()
	orderBy = current_app.config["ORDER_ZONA"]
	provincias = [item.Provincia for item in equipos_por_provincia]
	cantidades = [item.Cantidad for item in equipos_por_provincia]
	labels_json = json.dumps(provincias)
	cantidades_json = json.dumps(cantidades)
	return render_template('reporte.html',
							chart_type='pie',
							labels=labels_json,
							data=cantidades_json,
							datos_sql=equipos_por_provincia,
							orderBy = orderBy,
							nombre_reporte='Reporte equipos por Provincia',
							title='Reporte por zona',)


@reportes.route("/reporte_modelo")
@role_required("Admin")
def reporte_modelo():	
	query = db.session.query(
						Modelo.nombre.label('Modelo'),
						func.count(Equipment.id).label('Cantidad'))\
						.join(Equipment, Equipment.modelo_id == Modelo.id)\
						.group_by(Modelo.nombre)\
						.order_by(func.count(Equipment.id).desc())

	# Obtener los resultados
	equipos_por_modelo = query.all()
	orderBy = current_app.config["ORDER_ZONA"]
	modelos = [item.Modelo for item in equipos_por_modelo]
	cantidades = [item.Cantidad for item in equipos_por_modelo]
	labels_json = json.dumps(modelos)
	cantidades_json = json.dumps(cantidades)

	return render_template('reporte.html',
							chart_type='bar',
							labels=labels_json,
							data=cantidades_json,		
							datos_sql=equipos_por_modelo,
							orderBy = orderBy,
							nombre_reporte='Reporte equipos por Modelo',
							title='Reporte por modelo')