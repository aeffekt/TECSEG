let menuToggle = document.querySelector('.menu-toggle');
let menuHorizontal = document.querySelector('.menu-horizontal');

menuToggle.addEventListener('click', () => {
	menuHorizontal.classList.toggle('open');
});