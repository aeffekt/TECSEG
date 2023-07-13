from flask import  Blueprint, url_for, redirect, flash
from flask_login import login_required
from tseg.models import Equipment
from tseg import db
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle

prints = Blueprint('prints', __name__)


@prints.route("/print_etiqueta-<int:equipment_id>")
@login_required
def print_etiqueta(equipment_id):    
    try:
        equipo = Equipment.query.get_or_404(equipment_id)       
        heading = f'Etiqueta de equipo'
        modelo = equipo.modelo.nombre
        numSerie = equipo.numSerie
        homologacion = equipo.modelo.homologacion
        x, y = A4        
        numSerie_string = str(equipo.numSerie).replace('/', '-')
        path_etiqueta = f"./tseg/static/pdfs/{numSerie_string}.pdf"
        hoja_A4 = canvas.Canvas(path_etiqueta, pagesize=A4)

        font_size = 9  # Tamaño de fuente en puntos
        hoja_A4.setFont("Helvetica", font_size)  # Establecer el tamaño de fuente en el lienzo        

        hoja_A4.drawCentredString(100, y-50, heading)
        hoja_A4.drawCentredString(100, y-65, modelo)
        hoja_A4.drawCentredString(100, y-80, numSerie)

        hoja_A4.setLineWidth(0.5)

        hoja_A4.rect(65, y-55, 70, -44) #  X, Y, DeltaX, DeltaY
        hoja_A4.line(65, y-70, 135, y-70)
        hoja_A4.line(65, y-85, 135, y-85)

        if homologacion:
            hoja_A4.drawCentredString(100, y-95, homologacion.codigo)

        hoja_A4.save()
        flash(f"Se guardó la etiqueta correctamente. ",'success')

    except Exception as err:
        flash(f"Ocurrió un error al generar la etiqueta: {err}",'warning')
    finally:
        return redirect(url_for('equipments.equipment', equipment_id=equipo.id, filterBy='date_modified',filterOrder='desc'))