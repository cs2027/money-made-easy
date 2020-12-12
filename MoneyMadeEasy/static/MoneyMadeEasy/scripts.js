document.addEventListener('DOMContentLoaded', function() {
    // Have submit buttons change color when you hover over them
    document.querySelectorAll("input[type=submit]").forEach(function(element) {
        element.onmouseover = function() { change_background(this) };
        element.onmouseout = function() { revert_background(this) };
    });

    // Have main menu change color when you hover over them
    document.getElementById("main_menu").onmouseover = function() { change_background(this) };
    document.getElementById("main_menu").onmouseout = function() { revert_background(this) };

    // Have `delete` buttons change color (when user wants to delete an expense)
    document.querySelectorAll(".td_delete").forEach(function(element) {
        element.style.color = "Red";
        element.onmouseover = function() { change_color(this) };
        element.onmouseout = function() { revert_color(this) };
    });
});

// Change appearance if we hover over the aformentioned^^ elements
function change_background(element) {
    element.style.backgroundColor = "LightGray"; 
}

function revert_background(element) {
    element.style.backgroundColor = "White";
}

function change_color(element) {
    element.style.color = "#CC0000";
    element.style.textDecoration = "underline";
    element.style.cursor = "pointer";
}

function revert_color(element) {
    element.style.color = "Red";
    element.style.textDecoration = "none";
}
 