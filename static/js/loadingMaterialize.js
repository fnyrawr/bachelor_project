/* init JS elements */
document.addEventListener('DOMContentLoaded', function() {
    /* Modals */
    var modal_elems = document.querySelectorAll('.modal');
    var modal_instances = M.Modal.init(modal_elems);
    /* Sidenav */
    var sidenav_elems = document.querySelectorAll('.sidenav');
    var sidenav_instances = M.Sidenav.init(sidenav_elems);
    /* Dropdown elements */
    var dropdown_elems = document.querySelectorAll('.dropdown-trigger');
    var dropdown_instances = M.Dropdown.init(dropdown_elems);
    /* Tabs */
    var tabs = document.querySelectorAll('.tabs');
    for (var i = 0; i < tabs.length; i++){
    	M.Tabs.init(tabs[i]);
    };
    /* Form elements */
    var form_elems = document.querySelectorAll('input#input_text, textarea#textarea2');
    var form_instances = M.CharacterCounter.init(form_elems);
    /* Form select */
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems);
    /* Collapsibles */
    var collapsible_elems = document.querySelectorAll('.collapsible');
    var collapsible_instances = M.Collapsible.init(collapsible_elems);
    /* Datepickers */
    var picker_elems = document.querySelectorAll('.datepicker');
    var picker_instances = M.Datepicker.init(picker_elems, {
        format: 'yyyy-mm-dd',
        firstDay: 1,
        showClearBtn: true
    });
    /* Material Box */
    var mbox_elems = document.querySelectorAll('.materialboxed');
    var mbox_instances = M.Materialbox.init(mbox_elems);
    /* Tooltips */
    var elems = document.querySelectorAll('.tooltipped');
    var instances = M.Tooltip.init(elems);
});