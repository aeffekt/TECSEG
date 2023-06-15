# Programa de servicio de postventa par la empresa LIE SRL
# Diseñado y desaroolado por: Agustin Arnaiz

from tseg import create_app

app = create_app()

if __name__ == "__main__":
	app.run(debug=True)
	