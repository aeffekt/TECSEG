
// Funcion para captar el codigo postal y buscar GEOLOCALIZACION
document.addEventListener('DOMContentLoaded', function() {  
	let codigoPostalInput = document.getElementById('codigo_postal');
	let paisInput = document.querySelector('.paisSelect')
	let provinciaInput = document.querySelector('.provinciaSelect')
	let localidadInput = document.querySelector('.localidadSelect')

	 // Función para actualizar los campos de país, provincia y localidad
	 function actualizarCamposGeograficos(codigoPostal) {  
		if(codigoPostal!='')
		{
			// Realizar una solicitud al servidor para obtener los datos geográficos
			fetch(`/obtener-datos-geograficos?codigo_postal=${codigoPostal}`)
			.then(response => response.json())
			.then(data => {				
				if(data.localidad != null){
					pais = data.pais
					provincia = data.provincia
					localidad = data.localidad
					return fetch(`/obtener-datos-provincias?pais=${pais}`)
				}
				else{					
					limpiar_domicilio()
				}				
			})		  
			.then(response => response.json())
			.then(data => {				
				$('#provinciaSelect').empty()
				data.provincias_list.forEach(provincia => {
					$('#provinciaSelect').append(`<option value="${provincia}">${provincia}</option>`)
				})
				return fetch(`/obtener-datos-localidades?provincia=${provincia}`)
			})
			.then(response => response.json())
			.then(data => {
				$('#localidadSelect').empty();			
				data.localidades_list.forEach(localidad => {
					$('#localidadSelect').append(`<option value="${localidad}">${localidad}</option>`)
				})
				$('#paisSelect').val(pais).trigger('change')			
				$('#provinciaSelect').val(provincia).trigger('change')
				$('#localidadSelect').val(localidad).trigger('change')				
			})
			.catch(error => console.error('Error:', error));
		}
		else{
			limpiar_domicilio()
		}
		paisInput.disabled = false
		provinciaInput.disabled = false
		localidadInput.disabled = false
	}

	function limpiar_domicilio(){
		$('#paisSelect').val(null).trigger('change');
		$('#provinciaSelect').val(null).trigger('change');
		$('#localidadSelect').val(null).trigger('change');
		paisInput.disabled = false
		provinciaInput.disabled = true
		localidadInput.disabled = true
	}

	  
	// SELECT FUNCS
	function paisSelected(pais) {
		paisInput.disabled = false
		provinciaInput.disabled = false
		localidadInput.disabled = false
		fetch(`/obtener-datos-provincias?pais=${pais}`)
			.then(response => response.json())
			.then(data => {				
				// vacia la lista para cargar la nueva lista del select
				$('#provinciaSelect').empty();
				data.provincias_list.forEach(provincia => {
					$('#provinciaSelect').append(`<option value="${provincia}">${provincia}</option>`)
				});
				$('#provinciaSelect').val(null).trigger('change')
				$('#localidadSelect').val(null).trigger('change')
				})
			.catch(error => console.error('Error:', error))		
	}

	function provinciaSelected(provincia) {
		paisInput.disabled = false
		provinciaInput.disabled = false
		localidadInput.disabled = false
		fetch(`/obtener-datos-localidades?provincia=${provincia}`)
			.then(response => response.json())
			.then(data => {				
			// vacia la lista para cargar la nueva lista del select
			$('#localidadSelect').empty();			
			data.localidades_list.forEach(localidad => {
				$('#localidadSelect').append(`<option value="${localidad}">${localidad}</option>`);
			});
			$('#localidadSelect').val(null).trigger('change');			
			})
			.catch(error => console.error('Error:', error))		
	}

	function localidadSelected(localidad) {		
		fetch(`/obtener-dato-cp?localidad=${localidad}`)
			.then(response => response.json())
			.then(data => {
				codigoPostalInput.value = data.cp
			})
			.catch(error => console.error('Error:', error))			
	}

	// UNSELECT FUNCS
	function paisUnSelect() {		
		paisInput.disabled = false
		provinciaInput.disabled = true
		localidadInput.disabled = true
		$('#paisSelect').val(null).trigger('change')
		$('#provinciaSelect').val(null).trigger('change')
		$('#localidadSelect').val(null).trigger('change')
	}

	function provinciaUnSelect() {		
		paisInput.disabled = false
		provinciaInput.disabled = false
		localidadInput.disabled = true
		$('#provinciaSelect').val(null).trigger('change')
		$('#localidadSelect').val(null).trigger('change')
	}

	function localidadUnSelect() {
		paisInput.disabled = true
		provinciaInput.disabled = false
		localidadInput.disabled = false	
		$('#localidadSelect').val(null).trigger('change')
		codigoPostalInput.value = ''
	}

	// EVENTOS:
	codigoPostalInput.addEventListener('change', (event) => {
		let codigoPostal = event.target.value;
		actualizarCamposGeograficos(codigoPostal);
	  });
	
	// SELECT
	$('.paisSelect').on('select2:select', function (event) {
		let pais = event.params.data
		paisSelected(pais.id)
	});
	$('.provinciaSelect').on('select2:select', function (event) {
		var provincia = event.params.data
		provinciaSelected(provincia.id)
	});
	$('.localidadSelect').on('select2:select', function (event) {
		var localidad = event.params.data
		localidadSelected(localidad.id)
	});
	// UNSELECT
	$('.paisSelect').on('select2:unselect', function (event) {		
		paisUnSelect()
	});
	$('.provinciaSelect').on('select2:unselect', function (event) {		
		provinciaUnSelect()
	});
	$('.localidadSelect').on('select2:unselect', function (event) {		
		localidadUnSelect()
	});	
});
