cuit_input.oninput = function() {
    let inputValue = this.value;

    // Agregamos las clases CSS según la cantidad de dígitos ingresados
    if (inputValue.length === 11) 
    {
        cuit_input.classList.remove('input-red');
        cuit_input.classList.remove('input-orange');
        cuit_input.classList.add('input-green');
    } 
    else if (inputValue.length > 11)
    {
        cuit_input.classList.remove('input-green');
        cuit_input.classList.remove('input-orange');
        cuit_input.classList.add('input-red');
    } 
    else if (inputValue.length < 11)
    {
        cuit_input.classList.remove('input-green');
        cuit_input.classList.remove('input-red');
        cuit_input.classList.add('input-orange');
    } 
    else 
        cuit_input.classList.remove('input-green', 'input-red');
};