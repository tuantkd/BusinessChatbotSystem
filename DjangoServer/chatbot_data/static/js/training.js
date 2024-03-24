$(document).ready(function() {
    const baseUrl = window.location.origin;
    const pathName = window.location.pathname;
    const currentUrl = `${baseUrl}${pathName}`;
    const csrftoken = getCookie('csrftoken');
    var searchResults = [];

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken, // Include CSRF token in the request header
        };
        return headers;
    }

    $('.nav-link').click(function() {
        const targetId = $(this).attr('data-target');
        $('.nav-item').removeClass('active'); // Remove active class from all nav items
        $('.tab-pane').removeClass('active'); // Remove active class from all tab panes
        $('.nav-link').removeClass('active'); // Remove active class from all tabs
        $(this).addClass('active'); // Add active class to the clicked tab
        $(this).closest('.nav-item').addClass('active'); // Add active class to the parent nav item
        $(targetId).addClass('active'); // Add active class to the target tab pane
    });

    function init() {
        const loadTrainingDataUrl = `${currentUrl}/load_training_data`;
        const headers = getHeaders();
        $.ajax({
            url: loadTrainingDataUrl,
            type: 'GET',
            headers: headers,
            success: function(data) {
                // Handle the returned data here
                console.log(data);
            
                $('#raw_data > textarea').val(data.raw);
                $('#config > textarea').val(data.config);
                $('#nlu_data > textarea').val(data.nlu);
                $('#stories > textarea').val(data.stories);
                $('#domain > textarea').val(data.domain);
            },
            error: function(error) {
                // Handle errors here
                console.log(error);
            }
        });
    }

    init();
});