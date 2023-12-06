from tseg.models import Provincia, Localidad, Pais


# obtener_informacion_geografica
def obtener_informacion_geografica(codigo_postal):	
	localidad = ''
	provincia = ''
	pais = ''
	localidad = Localidad.query.filter_by(cp=codigo_postal).first()
	if localidad:
		provincia = Provincia.query.filter(Provincia.id==localidad.provincia_id).first()
		pais = Pais.query.filter(Pais.id==provincia.pais_id).first()
		localidad = localidad.nombre
		provincia = provincia.nombre
		pais = pais.nombre	
	return localidad, provincia, pais


def populate_pais():
	lista_pais = [p.nombre for p in Pais.query.order_by(Pais.nombre.asc()).all()]	
	return lista_pais

def populate_provincia(pais):	
	pais = Pais.query.filter_by(nombre=pais).first()	
	lista_provincia = [p.nombre for p in Provincia.query.filter_by(pais_id=pais.id).order_by(Provincia.nombre.asc()).all()]
	return lista_provincia

def populate_localidad(provincia):	
	provincia = Provincia.query.filter_by(nombre=provincia).first()	
	lista_localidad =  [l.nombre for l in Localidad.query.filter_by(provincia_id=provincia.id).all()]	
	return lista_localidad