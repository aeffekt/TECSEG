// setea null los select que se cargaron con un key = -1, ademas elimina este opcion del select
function limpiarSeleccion(selectId) {
			if ($(selectId).val() === '-1') {
                $(selectId).find('option:selected').remove();
				$(selectId).val(null, null).trigger('change');
			}
		}