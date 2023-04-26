$(document).ready(function(){
    $('.sidenav').sidenav();
    $('select').formSelect();
    $('.materialboxed').materialbox();
    $('.modal').modal();
    $(".dropdown-trigger").dropdown();
    $('.parallax').parallax();
    $('.carousel').carousel();
    $('.collapsible').collapsible();
    $('.carousel.carousel-slider').carousel({
        fullWidth: true,
        indicators: true
    });
    $('.fixed-action-btn').floatingActionButton();
    $('.datepicker').datepicker({
        format: 'yyyy-mm-dd',
        showClearBtn: true
    });
    var elems = document.querySelectorAll('.fixed-action-btn');
});