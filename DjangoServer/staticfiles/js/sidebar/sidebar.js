document.addEventListener('DOMContentLoaded', function () {
    // Function to handle logout
    function logout() {
        // Here, you should replace '/logout-url/' with the actual path to your logout view in Django
        window.location.href = '/logout-url/';
    }

    // Assuming you have a logout button with an ID 'logout-btn'
    var logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }
});
