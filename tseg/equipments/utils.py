import os
from flask import current_app, url_for, flash
from tseg import db
from datetime import datetime
from tseg.users.utils import dateFormat
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfReader, PdfWriter


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
	caratula_a4.drawString(180, y-480, f"{tipo_equipo} {equipo.modelo.nombre}")	
	caratula_a4.drawString(180, y-500, f"banda {rango}")
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
		

# subir archivos a equipo
def upload_files(files, equipment):
    if files and files[0].filename!='':        
        folder_path = get_full_folder_path(equipment)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        for file in files:			
            file.save(f'{folder_path}//{file.filename}') # Then save the file


# devuelve el nombre de la carpeta de archivos de un equipo
def get_folder_name(equipment):
    numero_serie = f'{equipment.detalles_trabajo.orden_trabajo.codigo}-{equipment.numSerie}'
    folder_name = numero_serie.replace('/','-')
    return folder_name


# devuelve el nombre de carpeta para archivos de un equipo (sirve para el path del template)
def get_folder_path(equipment):
    folder_name = get_folder_name(equipment)
    folder_path = url_for("static", filename=f'upload_files/{folder_name}/')
    return folder_path


# devuelve la ruta completa de la carpeta de archivos del equipo (sirve para obtener la info completa de files)
def get_full_folder_path(equipment):
    folder_name = get_folder_name(equipment)
    full_folder_path = os.path.join(current_app.root_path, f'static\\upload_files\\', folder_name)
    return full_folder_path


# retorna una lista con la info de los archivos en la carpeta del equipo
def get_files_info(folder_path):
	archivos_info = []
	if os.path.exists(folder_path):
		# Obtener una lista de archivos en la carpeta		
		archivos_en_carpeta = os.listdir(folder_path)
		for archivo in archivos_en_carpeta:
			archivo_path = os.path.join(folder_path, archivo)			
			if os.path.isfile(archivo_path):
				# Obtener el tamaño del archivo en bytes
				size = os.path.getsize(archivo_path)
				path = archivo_path
				# Obtener la fecha de creación del archivo (en segundos desde la época)				
				creation_time = dateFormat()
				archivos_info.append({
					'nombre': archivo,
					'tamaño': size,
					'ruta': path,
					'fecha_creacion': creation_time
				})			
	return archivos_info


# borrar archivo de equipo en el servidor
def delete_file(file_path, file_name):
	path = os.path.join(current_app.root_path, file_path+"/"+file_name)	
	if os.path.exists(path):
		try:
			os.remove(path)
			flash("El archivo se eliminó correctamente", 'success')
		except:
			flash(f"Ocurrió un error al intentar eliminar el archivo {file_name}", 'warning')
	