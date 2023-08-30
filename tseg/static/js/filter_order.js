// Pone en la barra de navegacion los valores de orderBy y orderOrder
document.getElementById('filterButton').addEventListener('click', function() {
    let url = new URL(window.location.href);
    let selectItem = document.getElementById('selectItem').value;
    let orderBy = document.getElementById('orderBy').value;
    let orderOrder = document.getElementById('orderOrder').value;
    
    //deshabilitado, ver en toolbar.html y utils.js
    //let datepicker1 = document.getElementById('datepicker1').value;
    //let datepicker2 = document.getElementById('datepicker2').value;    

    url.searchParams.set('selectItem', selectItem);
    url.searchParams.set('orderBy', orderBy);
    url.searchParams.set('orderOrder', orderOrder);
    //url.searchParams.set('datepicker1', datepicker1);
    //url.searchParams.set('datepicker2', datepicker2);
    
    window.location.href = url;
});
