document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('edit-headquarters-address').addEventListener('click', function() {
        // Implement the edit functionality here
        window.location.href = '/admin/your_app_name/address/<ADDRESS_ID>/change/';
    });

    document.getElementById('add-headquarters-address').addEventListener('click', function() {
        // Implement the add functionality here
        window.location.href = '/admin/your_app_name/address/add/';
    });

    document.getElementById('view-headquarters-address').addEventListener('click', function() {
        // Implement the view functionality here
        window.location.href = '/admin/your_app_name/address/<ADDRESS_ID>/';
    });
});
