import os
import secrets
from PIL import Image
from flask import url_for,current_app, abort, request, flash
from flask_login import current_user
from flask_mail import Message
from tseg import mail, db
from functools import wraps
from datetime import datetime
from tseg.models import (Equipment, User, Historia, Orden_reparacion, Localidad, Provincia, Pais, 
						 Detalle_reparacion, Detalle_trabajo, Orden_trabajo, Client)
from sqlalchemy import asc, desc

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfReader, PdfWriter
from datetime import datetime


# obtener el nombre del atributo para filtrar la búsqueda
def buscarLista(dBModel, *arg):
	order_by = dBModel.__table__.columns.keys()[0]

	# Obtener los valores de filterBy y filterOrder desde la solicitud
	select_item = request.args.get('selectItem', '')
	if not select_item:
		# sino hay un elemento seleccionado, carga orden por parametro
		order_by = request.args.get('orderBy', order_by)
	
	sort_column = getattr(dBModel, order_by)

	# ORDEN
	order_order = request.args.get('orderOrder', 'desc')
	if order_order == "asc":
		orden = asc(sort_column)
	else:
		orden = desc(sort_column)

	# FECHAS (deshabilitado, ver en toolbar.html y filter_order.js)
	#date1 = request.args.get('datepicker1', '')
	#date2 = request.args.get('datepicker2', '')
			
	# Si el modelo tiene la columna "date_modified," ordenar por ella en segunda instancia
	#if hasattr(dBModel, 'date_modified'):
	#	sort_column = (sort_column, getattr(dBModel, 'date_modified'))

	lista = dBModel.query.order_by(orden)	

	if arg:
		# filtrado extra de Detalle Reparación
		if dBModel==Detalle_reparacion:
			# para un OR determinada
			if isinstance(arg[0], Orden_reparacion):
				lista = lista.filter_by(reparacion_id=arg[0].id)

		# filtrado extra de Equipos
		if dBModel==Equipment:
			# para un detalle trabajo determinado
			if isinstance(arg[0], Detalle_trabajo):
				lista = lista.filter_by(detalle_trabajo_id=arg[0].id)

		# filtrado extra de O.R.
		elif dBModel==Orden_reparacion:
			# ordenes de reparacion por tecnico
			if isinstance(arg[0], User):
				lista = lista.filter_by(tecnico_id=arg[0].id)

			# ordenes de reparacion por equipo
			if isinstance(arg[0], Equipment):
				lista = lista.filter_by(equipo_id=arg[0].id)
		
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
		
		# filtrado extra de Detalle trabajo
		elif dBModel==Detalle_trabajo:
			# para un OT determinada			
			if isinstance(arg[0], Orden_trabajo):				
				lista = lista.filter_by(trabajo_id=arg[0].id)
		
		# filtrado extra de Orden trabajo
		elif dBModel==Orden_trabajo:
			# para un cliente determinado
			if isinstance(arg[0], Client):				
				lista = lista.filter_by(client_id=arg[0].id)	
	return lista
	

# obtener_informacion_geografica
def obtener_informacion_geografica(codigo_postal):	
	localidad_nombre = ''
	provincia_nombre = ''
	pais_nombre = ''
	localidad = Localidad.query.filter_by(cp=codigo_postal).first()
	if localidad:
		provincia = Provincia.query.filter(Provincia.id==localidad.provincia_id).first()
		pais = Pais.query.filter(Pais.id==provincia.pais_id).first()
		localidad_nombre = localidad.nombre
		provincia_nombre = provincia.nombre
		pais_nombre = pais.nombre
	return localidad_nombre, provincia_nombre, pais_nombre;


# dar formato a la fecha actual NOW
def dateFormat():
	now = datetime.now()
	now = now.strftime("%Y-%m-%dT%H:%M:%S")
	return datetime.fromisoformat(now)


#guardar imagen en carpeta
def save_picture(form_picture, folder):
	img = Image.open(form_picture)
	
	random_hex = secrets.token_hex(8) #crea nombre random para la imagen elegida
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext #conserva la extension original del archivo
	picture_path = os.path.join(current_app.root_path, f'static\\{folder}', picture_fn)

	# se toma el ancho y alto de la imagen
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
	output_size = (right-left,bottom-top)
	img_cropped = img.crop((left, top, right, bottom))
	
	img_rgb = img_cropped.convert('RGB') # si es png o tiene trnassparencia se la quito asi evita errores
	img_rgb.thumbnail(output_size)
	img_rgb.save(picture_path)

	return picture_fn


# reset EMAIL
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('TECSEG - Reset de contraseña requerido',
                  sender='no-reply@tecseg.local',
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


# generar PDF etiqueta num serie
def print_etiqueta_pdf(path, equipo):
	homologacion = equipo.modelo.homologacion
	modelo = f'{equipo.modelo.nombre} {equipo.modelo.anio}'	
	numSerie = f'{equipo.detalle_trabajo.orden_trabajo.codigo}-{equipo.numSerie}'	
	# formateo del texto
	heading = f'Etiqueta de equipo'
	file_name_numSerie = str(f"{equipo.detalle_trabajo.orden_trabajo.codigo}-{equipo.numSerie}").replace('/', '_')		
	name_etiqueta = f"{file_name_numSerie}.pdf"	
	# config CANVAS
	x, y = A4
	hoja_A4 = canvas.Canvas(f"{path}{name_etiqueta}", pagesize=A4)
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
	try:
		# guardar datos
		hoja_A4.save()
		equipo.etiqueta_file = name_etiqueta		
		db.session.commit()
		flash(f"La etiqueta del número de serie se generó correctamente. ",'success')
	except Exception as err:
		flash(f"Ocurrió un error al generar la etiqueta del número de serie: {err}",'warning')


# Carátula de manual PDF
def print_caratula_pdf(path, equipo):
	modelo = f'{equipo.modelo.nombre} {equipo.modelo.anio}'
	marca = equipo.modelo.marca.nombre
	tipo_equipo = equipo.modelo.tipo_modelo.tipo
	numSerie = f'{equipo.detalle_trabajo.orden_trabajo.codigo}-{equipo.numSerie}'	
	cliente = f"{equipo.detalle_trabajo.orden_trabajo.client.nombre} {equipo.detalle_trabajo.orden_trabajo.client.apellido}"
	domicilio=f"{equipo.detalle_trabajo.orden_trabajo.client.domicilio.localidad.nombre} ({equipo.detalle_trabajo.orden_trabajo.client.domicilio.localidad.provincia.nombre})"
	otn = f"{equipo.detalle_trabajo.orden_trabajo.codigo}"	
	canalFrec = equipo.frecuencia_eq.canal
	rango = equipo.frecuencia_eq.rango
	if str(rango) == "MHz":
		tipoCanalFrec="FRECUENCIA: "		
		canalFrec = str(canalFrec)+" "+str(rango)
		rango = 'FM'
	else:
		tipoCanalFrec="CANAL: "	
	# formateo del texto
	file_name_caratula = str(f"{equipo.detalle_trabajo.orden_trabajo.codigo}-{equipo.numSerie}_caratula").replace('/', '_')
	name_caratula = f"{file_name_caratula}.pdf"	
	# config CANVAS
	x, y = A4
	caratula_a4 = canvas.Canvas(f"{path}{name_caratula}", pagesize=A4)
	caratula_a4.setFont("Helvetica-Bold", 18)  # Establecer el tamaño de fuente en el lienzo	
	# texto de la etiqueta
	caratula_a4.drawString(70, y-450, 'MARCA :')
	caratula_a4.drawString(180, y-450, marca)
	caratula_a4.drawString(70, y-480, 'EQUIPO :')
	caratula_a4.setFont("Helvetica-Bold", 15)
	caratula_a4.drawString(180, y-480, f"{tipo_equipo} {equipo.modelo.nombre} banda {rango}")	
	caratula_a4.setFont("Helvetica-Bold", 18)
	caratula_a4.drawString(70, y-530, 'MODELO :')
	caratula_a4.drawString(180, y-530, modelo)
	caratula_a4.setFont("Helvetica-Bold", 15)
	caratula_a4.drawString(70, y-560, tipoCanalFrec)
	caratula_a4.setFont("Helvetica-Bold", 18)
	caratula_a4.drawString(180, y-560, canalFrec)
	caratula_a4.setFont("Helvetica-Bold", 15)
	caratula_a4.drawString(70, y-600, 'DESTINO :')
	caratula_a4.drawString(180, y-600, cliente)
	caratula_a4.drawString(180, y-620, domicilio)
	caratula_a4.drawString(70, y-660, 'SERIE :')
	caratula_a4.drawString(180, y-660, numSerie)
	caratula_a4.drawString(380, y-660, 'O.T.Nº :')
	caratula_a4.drawString(440, y-660, otn)
	caratula_a4.drawString(70, y-690, 'FECHA :')
	caratula_a4.drawString(180, y-690, datetime.now().strftime("%d/%m/%y"))	
	try:
		# guardar datos caratula PDF
		caratula_a4.save()
		equipo.caratula_file = name_caratula
		db.session.commit()
		# abre la caratula vacie y hace merge con la nueva hoja PDF
		existing_pdf = PdfReader(f'{path}caratula.pdf', "rb")	
		output = PdfWriter()
		new_pdf = PdfReader(f'{path}{name_caratula}', "rb")
		page = existing_pdf.pages[0]
		page.merge_page(new_pdf.pages[0])
		output.add_page(page)	
		output.write(f'{path}{name_caratula}')
		flash(f"La carátula de manual se generó correctamente. ",'success')
	except Exception as err:
		flash(f"Ocurrió un error al generar la carátula del manual: {err}",'warning')