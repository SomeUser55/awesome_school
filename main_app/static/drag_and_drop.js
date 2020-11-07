
Sortable.create(items_to_select, {
    animation: 100,
    group: 'list-1',
    draggable: '.list-group-item',
    handle: '.list-group-item',
    sort: true,
    filter: '.sortable-disabled',
    chosenClass: 'active'
});


Sortable.create(items_selected, {
    animation: 100,
    group: 'list-1',
    draggable: '.list-group-item',
    handle: '.list-group-item',
    sort: true,
    filter: '.sortable-disabled',
    chosenClass: 'active'
});


$("#submit_selected").on("click",
    function(e){
        // e.preventDefault();

        $("#items_selected").sortable();
        var idsInOrder = $("#items_selected").sortable("toArray");

        document.getElementById("ids_selected").value = idsInOrder.join(',');
        $("#myform").submit();
});