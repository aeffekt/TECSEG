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




// THEME COLOR CHANGER
      window.addEventListener("DOMContentLoaded", function() {
        var icon = document.getElementById("icon");
        var body = document.body;

        // Recuperar el estado del tema del almacenamiento local
        var theme = localStorage.getItem("theme");
          if (theme === "light") {
        body.classList.add("theme-light");
          }

        icon.onclick = function() {
            body.classList.toggle("theme-light");
            document.body.style.transition = '2s';
            if(document.body.classList.contains("theme-light")){
              icon.src = "{{ url_for('static', filename='images/theme_light.png') }}";
              icon.title = "Cambiar a modo oscuro";
            }else{
              icon.src = "{{ url_for('static', filename='images/theme_dark.png') }}";
              icon.title = "Cambiar a modo claro";
            }

            // Guardar el estado del tema en el almacenamiento local
            if (body.classList.contains("theme-light")) {
              localStorage.setItem("theme", "light");
            } 
            else{
              localStorage.setItem("theme", "dark");
            }
        };
      });

      // THEME COLOR CALL
      function cambiarColor() {
        var selectElement = document.getElementById("estadoSelect");
        var selectedOption = selectElement.options[selectElement.selectedIndex];
        selectElement.className = selectedOption.className + " selected";
      }
   
    // convierte un SELECT a CHOSEN
      $(".chosen").chosen({
          search_contains: true,
          no_results_text: 'No se encontró: ',
          width: '100%',
          max_shown_results: 100,  
        });

      // Pone en la barra de navegacion los valores de filterBy y filterOrder
    document.getElementById('filterButton').addEventListener('click', function() {
      var filterBy = document.getElementById('filterBy').value;
          var filterOrder = document.getElementById('filterOrder').value;
          var url = new URL(window.location.href);
          url.searchParams.set('filterBy', filterBy);
          url.searchParams.set('filterOrder', filterOrder);
          window.location.href = url;
    });