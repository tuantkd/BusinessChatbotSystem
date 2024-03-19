$(document).ready(function() {
    // Toggle Aside Menu
    function toggleAside() {
        if ($("body").hasClass("aside-menu-hidden")) {
            $("body").removeClass("aside-menu-hidden").addClass("aside-menu-fixed");
        } else {
            $("body").removeClass("aside-menu-fixed").addClass("aside-menu-hidden");
        }
    }

    // Toggle Sidebar
    function toggleSidebar() {
        if ($("body").hasClass("sidebar-fixed")) {
            $("body").removeClass("sidebar-fixed").addClass("sidebar-hidden");
        } else {
            $("body").addClass("sidebar-fixed").removeClass("sidebar-hidden");
        }
    }

    // Logout function could be handled differently based on your backend logic.
    // Here's a simple way to redirect to a logout URL. Adjust the URL as needed.
    function logout() {
        // Assuming you have a Django view handling logout at '/logout/'
        window.location.href = '/logout/';
    }

    // Bind events to elements
    // Example: Assuming you have buttons or links with specific IDs or classes for these actions
    $('#toggle-aside-btn').click(toggleAside);
    $('#toggle-sidebar-btn').click(toggleSidebar);
    $('#logout-btn').click(logout);
});
