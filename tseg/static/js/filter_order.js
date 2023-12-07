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
let orderByElement = document.getElementById('orderBy')
let orderOrderElement = document.getElementById('orderOrder')
if (orderByElement)
    orderByElement.addEventListener('change', toolbar_js)
if (orderOrderElement)
    orderOrderElement.addEventListener('change', toolbar_js)
// captura con el boton el elemento del select2
let filterButton = document.getElementById('filterButton');
if (filterButton) {
    filterButton.addEventListener('click', function() {   
        let url = new URL(window.location.href);
        let selectItem = document.getElementById('selectItem').value;
        url.searchParams.set('selectItem', selectItem);
        window.location.href = url;
    });
}