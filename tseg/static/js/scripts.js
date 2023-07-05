//  FUNCION PARA VOLVER A PÁGINA ANTERIOR
function goBack() {
  window.history.back();
}


// Funcion para captar el codigo postal y buscar GEOLOCALIZACION
document.addEventListener('DOMContentLoaded', function() {
  console.log('Llamando a la función actualizarCamposGeograficos');
  // COMPLETA PAIS, PROVINCIA y LOCALIDAD a partir de Codigo postal
  const codigoPostalInput = document.getElementById('codigo_postal');
  const paisInput = document.getElementById('pais');
  const provinciaInput = document.getElementById('provincia');
  const localidadInput = document.getElementById('localidad');

  // Función para actualizar los campos de país, provincia y localidad
  function actualizarCamposGeograficos(codigoPostal) {
    console.log('Llamando a la función actualizarCamposGeograficos');
    // Realizar una solicitud al servidor para obtener los datos geográficos
    fetch(`/obtener-datos-geograficos?codigo_postal=${codigoPostal}`)
      .then(response => response.json())
      .then(data => {
        // Actualizar los valores de los campos correspondientes
        paisInput.value = data.pais;
        provinciaInput.value = data.provincia;
        localidadInput.value = data.localidad;
      })
      .catch(error => console.error('Error:', error));
  }

  // Evento para detectar cambios en el campo de código postal
  codigoPostalInput.addEventListener('change', (event) => {
    const codigoPostal = event.target.value;
    actualizarCamposGeograficos(codigoPostal);
  });
});



