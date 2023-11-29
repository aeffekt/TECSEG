
// Funcion para captar el codigo postal y buscar GEOLOCALIZACION
document.addEventListener('DOMContentLoaded', function() {  
  // COMPLETA PAIS, PROVINCIA y LOCALIDAD a partir de Codigo postal
  const codigoPostalInput = document.getElementById('codigo_postal');  

  // Función para actualizar los campos de país, provincia y localidad
  function actualizarCamposGeograficos(codigoPostal) {    
    // Realizar una solicitud al servidor para obtener los datos geográficos
    fetch(`/obtener-datos-geograficos?codigo_postal=${codigoPostal}`)
      .then(response => response.json())
      .then(data => {
        // Actualizar los valores de los campos correspondientes
        $('#paisSelect').val(data.pais).trigger('change');
        $('#provinciaSelect').val(data.provincia).trigger('change');
        $('#localidadSelect').val(data.localidad).trigger('change');        
      })
      .catch(error => console.error('Error:', error));
  }

  // Evento para detectar cambios en el campo de código postal
  codigoPostalInput.addEventListener('change', (event) => {
    const codigoPostal = event.target.value;
    actualizarCamposGeograficos(codigoPostal);
  });
  
});
