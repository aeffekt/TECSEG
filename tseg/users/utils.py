import os
from PIL import Image
from flask import url_for,current_app, abort, request, flash
from flask_login import current_user
from flask_mail import Message
from tseg import mail, db
from functools import wraps
from datetime import datetime
from tseg.models import (Equipment, User, Historia, Orden_reparacion, Localidad, Provincia, Pais, 
						 Detalle_reparacion, Detalle_trabajo, Orden_trabajo, Client, ErrorLog, dateFormat)
from sqlalchemy import asc, desc
import secrets
import traceback


# obtener el nombre del atributo para filtrar la búsqueda
def buscarLista(dBModel, *arg, toFilter=True):
	order_by = dBModel.__table__.columns.keys()[0]
	# Obtener los valores de filterBy y filterOrder desde la solicitud
	select_item = request.args.get('selectItem', '')
	if not select_item:		
		if toFilter:
			# si no hay un elemento seleccionado, carga orden por parametro
			order_by = request.args.get('orderBy', order_by)	
	sort_column = getattr(dBModel, order_by)
	# ORDEN
	order_order = request.args.get('orderOrder', 'desc')	
	if order_order == "asc":
		orden = asc(sort_column)
	else:
		orden = desc(sort_column)	
	lista = dBModel.query.order_by(orden, asc(dBModel.id))	
	# Filtros segun *ARG
	if arg:
		# filtrado extra de Equipos
		if dBModel==Equipment:
			# para un detalle trabajo determinado
			if isinstance(arg[0], Detalle_trabajo):
				lista = lista.filter_by(detalle_trabajo_id=arg[0].id)
		# filtrado extra Historias 
		elif dBModel==Historia:			
			# para un equipo determinado
			if isinstance(arg[0], Equipment):				
				lista = lista.filter_by(equipo_id=arg[0].id)
				if len(arg)==2:
					lista.filter_by(tipo_historia_id=arg[1])
			# para un usuario determinado
			if isinstance(arg[0], User):				
				lista = lista.filter_by(author_historia=arg[0])		
		# filtrado extra de O.R.
		elif dBModel==Orden_reparacion:			
			# ordenes de reparacion por tecnico
			if isinstance(arg[0], User):
				lista = lista.filter_by(tecnico_id=arg[0].id)
			# ordenes de reparacion por equipo
			if isinstance(arg[0], Equipment):				
				lista = lista.filter_by(equipo_id=arg[0].id)		
		# filtrado extra de Detalle Reparación
		elif dBModel==Detalle_reparacion:
			# para un OR determinada
			if isinstance(arg[0], Orden_reparacion):
				lista = lista.filter_by(reparacion_id=arg[0].id)		
		# filtrado extra de Orden trabajo
		elif dBModel==Orden_trabajo:
			# para un cliente determinado
			if isinstance(arg[0], Client):				
				lista = lista.filter_by(client_id=arg[0].id)
		# filtrado extra de Detalle trabajo
		elif dBModel==Detalle_trabajo:
			# para un OT determinada			
			if isinstance(arg[0], Orden_trabajo):				
				lista = lista.filter_by(trabajo_id=arg[0].id)
	return lista
	

#guardar imagen en carpeta
def save_picture(form_picture, folder):
	img_filename = secrets.token_hex(8) #crea nombre random para la imagen elegida
	_, f_ext = os.path.splitext(form_picture.filename)	
	picture_fn = img_filename + f_ext #conserva la extension original del archivo
	picture_path = os.path.join(current_app.root_path, f'static\\{folder}', picture_fn)
	img = Image.open(form_picture)
	img_rgb = img.convert('RGB') # si es png o tiene trnasparencia se la quito asi evita errores
	# Calcula las dimensiones del thumbnail respetando la relación de aspecto
	if folder=="profile_pics":		
		# se toma el ancho y alto de la imagen para hacer recorte cuadrado centrado
		width, height = img.size
		top = 0
		bottom = height
		left = 0
		right = width
		if width > height:		
			diff = (width - height)/2
			left = diff
			right = width - diff
		elif height > width:
			diff = (height - width)/2
			top = diff
			bottom = height - diff		
		img_rgb = img_rgb.crop((left, top, right, bottom))
		output_size = (125,125)
	else:
		output_size = (1024, 1024)  # Define el tamaño máximo del thumbnail
	img_rgb.thumbnail(output_size)
	img_rgb.save(picture_path)

	return picture_fn


# reset EMAIL
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('TECSEG - Reset de contraseña requerido',                  
				  sender=f'{current_app.config["MAIL_USERNAME"]}',
                  recipients=[user.email])
    msg.body = f'''Usuario: {user.username} \n Para resetear su contraseña use el siguiente link:
{url_for('users.reset_token', token=token, _external=True)}

Si ud no hizo este requerimiento, ignore este mensaje.'''
    mail.send(msg)


#control de ROL de usuario
def role_required(*roles):
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			if not current_user.role.role_name in roles:
				abort(403)  # Error 403: Acceso prohibido
			return func(*args, **kwargs)
		return wrapper
	return decorator


# filtro de fechas para reportes
def cargarFechasFiltroReportes():
	anioPredeterminado1 = current_app.config["ANIO1"]
	anioPredeterminado2 = current_app.config["ANIO2"]
	anio1 = request.args.get("anio1", anioPredeterminado1)
	anio2 = request.args.get("anio2", anioPredeterminado2)
	if anio2 > anio1:
		return anio1, anio2
	else:
		return anio2, anio1


# Error LOGGER
def error_logger(Exception):
	now = dateFormat()	
	error = ErrorLog(date_created=now,
					user_id=current_user.id,
					error=Exception,
					traceback=traceback.format_exc())		
	db.session.add(error)
	db.session.commit()	
	error_message_log = {"Hora": str(now),
					  "Usuario": str(current_user),
					  "Error": str(Exception)}
	current_app.logger.exception(error_message_log)
	flash('Ocurrió un error inesperado. Si el problema persiste consulte al administrador.', 'danger')
