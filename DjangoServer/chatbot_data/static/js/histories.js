$(document).ready(function() {
    function toggleList(button) {
        var list = button.nextElementSibling;
        list.style.display = (list.style.display === 'none' || list.style.display === '') ? 'block' : 'none';
    }
});