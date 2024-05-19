$(document).ready(function () {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    $('#upload-form').on('submit', function(e) {
        e.preventDefault();
        
        let formData = new FormData();
        formData.append('file', $('#file')[0].files[0]);
        
        $('#loading').show();  // Show loading spinner
        $('button').prop('disabled', true);  // Disable buttons

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function (data) {
                if (data.test_id) {
                    window.location.href = '/test/result/' + data.test_id;
                } else {
                    $('#loading').hide();  // Hide loading spinner
                    $('button').prop('disabled', false);  // Enable buttons
                }
            },
            error: function (error) {
                $('#loading').hide();  // Hide loading spinner
                $('button').prop('disabled', false);  // Enable buttons
                $('#result').html('<pre>' + error.responseText + '</pre>');
            }
        });
    });

    $('#upload-story-form').on('submit', function(e) {
        e.preventDefault();
        
        let formData = new FormData();
        formData.append('story_file', $('#story-file')[0].files[0]);
        
        $('#loading').show();  // Show loading spinner
        $('button').prop('disabled', true);  // Disable buttons

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function (data) {
                if (data.test_id) {
                    window.location.href = '/test/result/' + data.test_id;
                } else {
                    $('#loading').hide();  // Hide loading spinner
                    $('button').prop('disabled', false);  // Enable buttons
                }
            },
            error: function (error) {
                $('#loading').hide();  // Hide loading spinner
                $('button').prop('disabled', false);  // Enable buttons
                $('#result').html('<pre>' + error.responseText + '</pre>');
            }
        });
    });

    $('.delete-test').on('click', function() {
        var testId = $(this).data('test-id');
        if (confirm('Are you sure you want to delete this test?')) {
            $.ajax({
                url: '/chatbot/test/delete/' + testId + '/',
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                success: function(response) {
                    location.reload();
                },
                error: function(error) {
                    alert('Failed to delete the test.');
                    console.error('Error:', error);
                }
            });
        }
    });
});
