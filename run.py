# Programa desarrollado por Agustin Arnaiz a partir de: "Python Flask Tutorial: Full-Featured Web App", por Corey Schafer

from tseg import create_app

app = create_app()

if __name__ == "__main__":
	app.run(debug=True)
	