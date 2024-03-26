
$(document).ready(function () {
    function toggleAside() {
        if ($("body").hasClass("aside-menu-hidden")) {
            $("body").removeClass("aside-menu-hidden").addClass("aside-menu-fixed");
        } else {
            $("body").removeClass("aside-menu-fixed").addClass("aside-menu-hidden");
        }
    }

    function toggleSidebar() {
        if ($("body").hasClass("sidebar-fixed")) {
            $(".sidebar-fixed").addClass("sidebar-hidden").removeClass("sidebar-fixed");
        } else {
            $(".sidebar-hidden").addClass("sidebar-fixed").removeClass("sidebar-hidden");
        }
    }

    
    // Attach these functions to the relevant events
    // For example, if you have a button to toggle the sidebar:
    $(".navbar-toggler.layout-toggler").click(function (e) {
        e.preventDefault();
        toggleSidebar();
    });
    $("#asideToggleButton").click(toggleAside);
    

    // For logout, you would typically make a POST request to a Django view
    // that handles logout. Here is a simple example:
    $("#logoutButton").click(function () {
        $.post("{% url 'logout' %}", function () {
            location.reload();
        });
    });
});