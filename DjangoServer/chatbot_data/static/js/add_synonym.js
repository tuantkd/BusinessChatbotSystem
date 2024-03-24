$(document).ready(function() {
    const baseURL = window.location.origin;
    const pathName = window.location.pathname;
    const currentURL = baseURL + pathName;
    const previousURL = document.referrer;
    const csrftoken = getCookie('csrftoken');

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

    // $('#newsynonym').on('submit', function(event) {
    //     event.preventDefault();
    //     const addSynonymURL = currentURL;
    //     const headers = getHeaders();

    //     $.ajax({
    //         url: addSynonymURL,
    //         type: 'POST',
    //         headers: headers,
    //         data: $(this).serialize(),
    //         dataType: 'json',
    //         success: function(data) {
    //             console.log(data);
    //         },
    //         error: function(error) {
    //             // handle error
    //             console.log(error);
    //         }
    //     });
    // });
});