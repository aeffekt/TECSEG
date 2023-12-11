# reportes routes
from flask import render_template, Blueprint
from tseg import db
from tseg.models import (Orden_reparacion, Equipment, Role, User, 
						 Provincia, Pais, Domicilio, Localidad, Client, 
						 Detalle_trabajo, Orden_trabajo, Estado_or, Modelo, Marca)
from sqlalchemy import func
from tseg.users.utils import role_required, cargarFechasFiltroReportes
import json
from datetime import datetime


reportes = Blueprint('reportes', __name__)
current_year = datetime.now().year # Envia el año actual a los reportes para el tope de filtro

@reportes.route("/reporte_reparaciones")
@role_required("Admin", "ServicioCliente")
def reporte_reparaciones():	
	#filtrado de fechas
	fecha1, fecha2 = cargarFechasFiltroReportes()
	query = db.session.query(
				Modelo.nombre.label('Modelo'),
				func.count(Equipment.id).label('Cant'))\
					.join(Equipment, Equipment.modelo_id == Modelo.id)\
					.join(Orden_reparacion, Equipment.id == Orden_reparacion.equipo_id)\
					.filter(Equipment.anio >= fecha1, Equipment.anio <= fecha2)\
					.group_by(Modelo.nombre)\
					.order_by(func.count(Equipment.id).desc())
	# Obtener los resultados
	equipos_por_modelo = query.all()	
	modelos = [item.Modelo for item in equipos_por_modelo]
	cantidades = [item.Cant for item in equipos_por_modelo]
	labels_json = json.dumps(modelos)
	cantidades_json = json.dumps(cantidades)
	return render_template('reporte.html',
							chart_type='bar',
							labels=labels_json,
							data=cantidades_json,		
							datos_sql=equipos_por_modelo,							
							nombre_reporte='Reporte de O.R. por modelo de equipo',
							title='Reporte reparaciones',
							current_year=current_year)


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
	asignaciones_tecnicos = query.all()	
	tecnicos = [item.Técnico for item in asignaciones_tecnicos]
	cantidades = [item.Pendientes for item in asignaciones_tecnicos]
	labels_json = json.dumps(tecnicos)
	cantidades_json = json.dumps(cantidades)		
	return render_template('reporte.html',
							chart_type='bar',
							labels=labels_json,
							data=cantidades_json,
							datos_sql=asignaciones_tecnicos,							
							nombre_reporte='Reporte de O.R. Activas por técnico',
							title='Reporte técnicos',
							current_year=current_year)


@reportes.route("/reporte_zonal")
@role_required("Admin")
def reporte_zona():
	#filtrado de fechas
	fecha1, fecha2 = cargarFechasFiltroReportes()
	query = db.session.query(
					    Provincia.nombre.label('Provincia'),
						func.substring(Pais.nombre, 1, 3).label('Pais'),
					    func.count(Equipment.id).label('Cant')).\
						join(Provincia, Pais.provincias).\
						join(Localidad, Provincia.localidades).\
						join(Domicilio, Localidad.domicilios).\
						join(Client, Domicilio.clientes).\
						join(Orden_trabajo, Client.ordenes_trabajo).\
						join(Detalle_trabajo, Orden_trabajo.detalles_trabajo).\
						join(Equipment, Detalle_trabajo.equipments).\
						filter(Equipment.anio >= fecha1, Equipment.anio <= fecha2).\
						where(Equipment.numSerie != None).\
						group_by(Provincia.nombre).\
						order_by(func.count(Equipment.id).desc())
	# Obtener los resultados	
	equipos_por_provincia = query.all()	
	provincias = [item.Provincia for item in equipos_por_provincia]
	cantidades = [item.Cant for item in equipos_por_provincia]
	labels_json = json.dumps(provincias)
	cantidades_json = json.dumps(cantidades)
	return render_template('reporte.html',
							chart_type='pie',
							labels=labels_json,
							data=cantidades_json,
							datos_sql=equipos_por_provincia,
							nombre_reporte='Reporte de equipos LIE / IA instalados por Provincia',
							title='Reporte por zona',
							current_year=current_year)


@reportes.route("/reporte_modelo")
@role_required("Admin")
def reporte_modelo():	
		#filtrado de fechas
	fecha1, fecha2 = cargarFechasFiltroReportes()
	query = db.session.query(
						Modelo.nombre.label('Modelo'),
						func.substring(Marca.nombre, 1, 3).label('Marca'),
						func.count(Equipment.id).label('Cant'))\
						.join(Equipment, Equipment.modelo_id == Modelo.id)\
						.join(Marca, Marca.id == Modelo.marca_id)\
						.filter(Equipment.anio >= fecha1, Equipment.anio <= fecha2)\
						.where(Equipment.numSerie != None)\
						.group_by(Modelo.nombre)\
						.order_by(func.count(Equipment.id).desc())
	# Obtener los resultados
	equipos_por_modelo = query.all()	
	modelos = [item.Modelo for item in equipos_por_modelo]
	cantidades = [item.Cant for item in equipos_por_modelo]
	labels_json = json.dumps(modelos)
	cantidades_json = json.dumps(cantidades)
	return render_template('reporte.html',
							chart_type='bar',
							labels=labels_json,
							data=cantidades_json,		
							datos_sql=equipos_por_modelo,							
							nombre_reporte='Reporte de equipos LIE / IA vendidos por Modelo',
							title='Reporte por modelo',
							current_year=current_year)


@reportes.route("/reporte_anio")
@role_required("Admin")
def reporte_anio():
	#filtrado de fechas
	fecha1, fecha2 = cargarFechasFiltroReportes()
	query = db.session.query(
						Equipment.anio.label('Año'),
						func.count(func.distinct(Orden_trabajo.id)).label('O.T.s'),
						func.count(Equipment.id).label('Equipos'))\
						.join(Detalle_trabajo, Detalle_trabajo.id == Equipment.detalle_trabajo_id)\
						.join(Orden_trabajo, Orden_trabajo.id == Detalle_trabajo.trabajo_id)\
						.filter(Equipment.anio >= fecha1, Equipment.anio <= fecha2)\
						.where(Equipment.numSerie != None)\
						.group_by(Equipment.anio)\
						.order_by(Equipment.anio.desc())
	# Obtener los resultados
	equipos_por_anio = query.all()	
	anios = [item.Año for item in equipos_por_anio]
	cantidades = [item.Equipos for item in equipos_por_anio]
	labels_json = json.dumps(anios)
	cantidades_json = json.dumps(cantidades)
	return render_template('reporte.html',
							chart_type='line',
							labels=labels_json,
							data=cantidades_json,
							datos_sql=equipos_por_anio,
							nombre_reporte='Reporte de ventas de equipos LIE / IA por año',
							title='Reporte de ventas',
							current_year=current_year)
