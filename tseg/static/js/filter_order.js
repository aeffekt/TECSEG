// Pone en la barra de navegacion los valores de orderBy y orderOrder
document.getElementById('filterButton').addEventListener('click', function() {
    var selectItem = document.getElementById('selectItem').value;
    var orderBy = document.getElementById('orderBy').value;
    var orderOrder = document.getElementById('orderOrder').value;
    var url = new URL(window.location.href);
    url.searchParams.set('selectItem', selectItem);
    url.searchParams.set('orderBy', orderBy);
    url.searchParams.set('orderOrder', orderOrder);
    window.location.href = url;
});
