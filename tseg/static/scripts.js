function cambiarColor() {
  var selectElement = document.getElementById("estadoSelect");
  var selectedOption = selectElement.options[selectElement.selectedIndex];
  selectElement.className = selectedOption.className + " selected";
}