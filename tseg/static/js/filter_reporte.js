// Pone en la barra de navegacion los valores de orderBy y orderOrder
document.getElementById('filterAnioButton').addEventListener('click', function() {
    let url = new URL(window.location.href);
    
    let anio1 = document.getElementById('anio1').value;
    let anio2 = document.getElementById('anio2').value;
    
    url.searchParams.set('anio1', anio1);
    url.searchParams.set('anio2', anio2);    
    
    window.location.href = url;
});
