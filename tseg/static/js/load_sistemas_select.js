function cargar_select_sistemas(dt_id){	
	fetch(`/get_sistemas?detalle_trabajo=${dt_id}`)
		.then(response => response.json())
		.then(data => {		
		// Actualizar los valores del select y evita se repitan en caso de update equipment
		for (const item in data) {			
			if (!$('#sistema').find('option:contains("' + data[item] + '")').length) {
				$('#sistema').append($("<option>", { text: data[item] }));
			}
		}
		})
		.catch(error => console.error('Error:', error));
}