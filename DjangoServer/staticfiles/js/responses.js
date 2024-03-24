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
        var actionId = $(this).data('target').split('_').pop();
        var addActionURL = currentUrl + '/add';
        // navigate to the add action page
        window.location.href = addActionURL ;
    });

    // Handle click event for the button with class 'btn-outline-danger'
    $('.btn-outline-danger').click(function () {
        var actionId = $(this).parent().find('.btn-outline-secondary').data('target').split('_').pop();

        $.ajax({
            url: '/api/action/' + actionId,  // Replace with your API endpoint
            type: 'DELETE',  // Replace with the type of request you want to make
            success: function (response) {
                // Handle success
                console.log(response);
            },
            error: function (error) {
                // Handle error
                console.log(error);
            }
        });
    });

});