
function highlight_nav_item(nav_item_id){
    var element = document.getElementById(nav_item_id);
    if (element !== null) {
        element.classList.add("active");
    }
}

window.onload = function() {
    var nav_item_id = document.getElementById("nav_item_id").textContent;
    highlight_nav_item(nav_item_id);
  };
