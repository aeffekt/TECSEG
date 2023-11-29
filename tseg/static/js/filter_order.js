// captura con el boton el elemento del select2
document.getElementById('filterButton').addEventListener('click', function() {   
    let url = new URL(window.location.href);
    let selectItem = document.getElementById('selectItem').value;
    url.searchParams.set('selectItem', selectItem);
    window.location.href = url;
});


// Pone en la barra de navegacion los valores de orderBy y orderOrder
function toolbar_js() {
    let url = new URL(window.location.href);
    let orderBy = document.getElementById('orderBy').value;
    let orderOrder = document.getElementById('orderOrder').value;        
    url.searchParams.set('orderBy', orderBy);
    url.searchParams.set('orderOrder', orderOrder);    
    window.location.href = url;
};

// captura los dos elementos del filtro
document.getElementById('orderBy').addEventListener('change', toolbar_js);
document.getElementById('orderOrder').addEventListener('change', toolbar_js);