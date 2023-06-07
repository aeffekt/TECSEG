
const temaOscuro = () => {
	document.querySelector("html").setAttribute("data-bs-theme", "dark")	
}

const temaClaro = () => {
	document.querySelector("html").setAttribute("data-bs-theme", "light")	
}

const cambiarTema = () => {
	document.querySelector("html").getAttribute("data-bs-theme") === "light"?
	temaOscuro() : temaClaro();
}