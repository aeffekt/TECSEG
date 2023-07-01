import os


class Config:	
	SECRET_KEY = os.getenv('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True # SECURITY 
	MAIL_USE_SSL = False
	MAIL_USERNAME = os.getenv('EMAIL_USER') #setear variable de entorno en S.O. servidor
	MAIL_PASSWORD = os.getenv('EMAIL_PASS') #IDEM, y reiniciar el sistema
	MAIL_DEBUG = True
	MAIL_DEFALUT_SENDER = None
	MAIL_MAX_EMAILS = 15
	MAIL_ASCII_ATTACHMENTS = False
	TEXTAREA_ROWS = 2
	FILTROS_USUARIOS = {"username": "Nombre",
					"role_id": "Tipo usuario"					
					}
	FILTROS_CLIENTES = {"id": "Número ID",
					"nombre": "Nombre",
					"apellido": "Apellido",
					"business_name": "Razón social"
					}
	FILTROS_EQUIPOS= {"anio": "Año de fabricación",
					"modelo_id": "Modelo",
					"marca_id": "Marca",
					"frecuencia_id": "Canal / Frecuencia",					
					"client_id": "Cliente",
					"numSerie": "Número de serie",					
					"date_created": "Fecha creado",
					"date_modified": "Fecha modificado",
					}
	FILTROS_MODELOS= {"nombre": "Nombre",
					"date_created": "Fecha creado",
					"date_modified": "Fecha modificado",					
					}
	FILTROS_HISTORIAS = {"date_modified": "Fecha modificado",
					"date_created": "Fecha creado",
					"title": "Título", 
					"tipologia_id": "Tipología",					
					"equipo_id": "equipo",
					}
	FILTROS_OR = {"estado_id": "estado",
					"codigo": "Código",					
					"tecnico_id": "Técnico asignado",
					"equipo_id": "equipo",					
					"date_created": "Fecha creado",
					"date_modified": "Fecha modificado",
					}

