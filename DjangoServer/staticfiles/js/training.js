$(document).ready(function() {
    $('#trainingForm').on('submit', function(e) {
        e.preventDefault();

        $.ajax({
            url: '/path/to/your/server/script', // replace with your server-side script URL
            method: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                // handle success
                console.log(response);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                // handle error
                console.error(textStatus, errorThrown);
            }
        });
    });
});