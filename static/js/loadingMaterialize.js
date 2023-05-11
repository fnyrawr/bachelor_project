$(document).ready(function(){
    $('.sidenav').sidenav();
    $('select').formSelect();
    $('.materialboxed').materialbox();
    $('.modal').modal();
    $('.dropdown-trigger').dropdown();
    $('.collapsible').collapsible();
    $('.datepicker').datepicker({
        format: 'yyyy-mm-dd',
        firstDay: 1,
        showClearBtn: true
    });
});