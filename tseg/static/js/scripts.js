//  FUNCION PARA VOLVER A PÁGINA ANTERIOR
function goBack() {
  window.history.back();
}

// abrir imagen en pantalla
function abrirImagen(src) {
  let ventana = window.open("", "_blank");
  ventana.document.write("<html><head><title>Imagen</title></head><body style='background: grey; margin: 0;'><h2>Click en pantalla para cerrar esta ventana y volver</h2><img src='" + src + "' style='max-width: 100%; max-height: 100vh; display: block; margin: auto;'/></body></html>");
  ventana.document.close();
  
  ventana.addEventListener('click', function() {
    ventana.close();
    });
  }