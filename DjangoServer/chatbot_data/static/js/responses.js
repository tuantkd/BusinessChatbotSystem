$(document).ready(function () {
    const intentId = window.location.pathname.split('/')[4];
    const baseUrl = window.location.origin;
    const pathName = window.location.pathname;
    const currentUrl = `${baseUrl}${pathName}`;
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

    function toggleResponseFields() {
        var selectedValue = $("#id_response_type").val();

        // Giả định #id_response_text và #id_response_file là các ID của trường bạn muốn ẩn/hiện
        if (selectedValue === "text") {
            $("#id_response_text").closest('p').show();
            $("#id_response_file").closest('p').hide();
        } else if (selectedValue === "image" || selectedValue === "video" || selectedValue === "audio") {
            $("#id_response_text").closest('p').hide();
            $("#id_response_file").closest('p').show();
        } else {
            $("#id_response_text").closest('p').hide();
            $("#id_response_file").closest('p').hide();
        }
    }

    // Gọi khi trang load để thiết lập trạng thái ban đầu
    toggleResponseFields();

    // Lắng nghe sự kiện thay đổi trên dropdown và gọi hàm để ẩn/hiện
    $("#id_response_type").change(toggleResponseFields);

    // Lấy đối tượng select
    var selectBot = document.getElementById('selectBot');
    // Lấy đối tượng span để hiển thị tên bot được chọn
    var selectedBotNameSpan = document.getElementById('selectedBotName');

    // Lắng nghe sự kiện thay đổi của select
    selectBot.addEventListener('change', function () {
        // Lấy option được chọn
        var selectedOption = selectBot.options[selectBot.selectedIndex];
        // Cập nhật nội dung của span
        selectedBotNameSpan.textContent = selectedOption.textContent;
    });

    // Handle click event for the button with class 'btn-outline-secondary'
    $('.btn-outline-secondary').click(function () {
        const targetTableId = $(this).data('target');
        const addResponseForm = $(`${targetTableId}`);
        addResponseForm.toggle('collapse');

    });

    // Handle click event for the button with class 'btn-outline-danger'
    $('.delete-action').click(function () {
        const actionId = $(this).parent().find('.btn-outline-secondary').data('target').split('_').pop();
        const deleteActionURL = currentUrl + '/delete_action';
        const headers = getHeaders();
        $.ajax({
            url: deleteActionURL,
            type: 'POST',
            headers: headers,
            data: JSON.stringify({ action_id: actionId }),
            success: function (response) {
                // Handle success
                console.log(response);
                // Remove the action from the DOM
                $(`#action_group_${actionId}`).remove();
                $(`#action_table_${actionId}`).remove();
            },
            error: function (error) {
                // Handle error
                console.log(error);
            }
        });
    });

    $('.btn-outline-success').click(function () {
        var responseType = $(this).closest('tr').find('select').val();
        var responseText = $(this).closest('tr').find('textarea').val();
        var parentElement = $(this).closest('.table-bordered');
        var actionId = parentElement.attr('id').split('_')[2];
        const addResponseURL = currentUrl + '/add_response';
        const headers = getHeaders();
        const data = {
            'action_id': actionId,
            'response_type': responseType,
            'response_text': responseText
        };
        $.ajax({
            url: addResponseURL,
            type: 'POST',
            headers: headers,
            data: JSON.stringify(data),
            success: function (response) {
                console.log(response);
                window.location.reload();
            },
            error: function (error) {
                console.log(error);
            }
        });
    });

    $('.btn-outline-info').click(function () {
        var responseType = $(this).closest('tr').find('select').val();
        var responseText = $(this).closest('tr').find('textarea').val();
        var parentElement = $(this).closest('.table-bordered');
        var actionId = parentElement.attr('id').split('_')[2];
        var responseId = $(this).closest('tr').attr('data-response-id');
        const updateResponseURL = currentUrl + '/update_response';
        const headers = getHeaders();
        const data = {
            'response_id': responseId,
            'action_id': actionId,
            'response_type': responseType,
            'response_text': responseText
        };
        $.ajax({
            url: updateResponseURL,
            type: 'POST',
            headers: headers,
            data: JSON.stringify(data),
            success: function (response) {
                console.log(response);
                window.location.reload();
            },
            error: function (error) {
                console.log(error);
            }
        });
    });

    $('.delete-response').click(function () {
        var responseId = $(this).closest('tr').attr('data-response-id');
        const currentRow = $(this).closest('tr');
        const deleteResponseURL = currentUrl + '/delete_response';
        const headers = getHeaders();
        $.ajax({
            url: deleteResponseURL,
            type: 'POST',
            headers: headers,
            data: JSON.stringify({ response_id: responseId }),
            success: function (response) {
                // Handle success
                console.log(response);
                // Remove the response from the DOM
                currentRow.remove();
            },
            error: function (error) {
                // Handle error
                console.log(error);
            }
        });
    });
});