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
	ORDER_USUARIOS = {"username": "Nombre",
					"role_id": "Tipo usuario"					
					}
	ORDER_CLIENTES = {"id": "Número ID",
					"nombre": "Nombre",
					"apellido": "Apellido",
					"business_name": "Razón social"
					}
	ORDER_EQUIPOS= {"date_modified": "Fecha modificado",
					"date_created": "Fecha creado",
					"anio": "Año de fabricación",
					"modelo_id": "Modelo",					
					"frecuencia_id": "Canal / Frecuencia",					
					"client_id": "Cliente",
					"numSerie": "Número de serie",
					"Marca.nombre": "Marca"
					}
	ORDER_MODELOS= {"nombre": "Nombre",
					"date_created": "Fecha creado",
					"date_modified": "Fecha modificado",					
					}
	ORDER_MARCAS= {"nombre": "Nombre"					
					}
	ORDER_HOMOLOGACION= {"codigo": "Código",
					"modelo": "Modelo",					
					}
	ORDER_HISTORIAS = {"date_modified": "Fecha modificado",
					"date_created": "Fecha creado",
					"title": "Título", 
					"tipologia_id": "Tipología",
					"equipo_id": "equipo",
					}
	ORDER_OR = {"estado_id": "Estado",
					"codigo": "Código",					
					"tecnico_id": "Técnico asignado",
					"equipo_id": "Equipo",					
					"date_created": "Fecha creado",
					"date_modified": "Fecha modificado",
					}
	ORDER_DETALLES = {"date_modified": "Fecha modificado",
					"date_created": "Fecha creado",					
					}
	ORDER_ZONA = {"cantidad": "Cantidad",
					"provincia": "Provincia",
					}
	ORDER_TECNICO = {"cantidad": "Cantidad",
					"username": "Nombre",
					}
