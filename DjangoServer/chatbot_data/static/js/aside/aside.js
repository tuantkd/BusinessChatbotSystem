$(document).ready(function () {
    // Khi người dùng nhấn nút "Go"
    $('#execute-test-request').on('click', function () {
        var testText = $('#test_text').val(); // Lấy giá trị từ input
        if (testText) {
            // Gửi yêu cầu POST đến endpoint mà bạn đã cấu hình trong Django
            $.ajax({
                url: '/api/rasa/model/parse', // Đường dẫn đến API của bạn
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ text: testText }),
                beforeSend: function () {
                    addOverlay(); // Hiển thị overlay hoặc loader
                },
                success: function (response) {
                    // Xử lý kết quả trả về từ server
                    console.log(response); // Log hoặc hiển thị kết quả
                    // Cập nhật UI tương ứng
                    // Ví dụ: Hiển thị kết quả trong một phần tử của trang
                    $('#response-text').text(JSON.stringify(response, null, 2));
                },
                error: function (error) {
                    console.error("There was an error processing your request", error);
                },
                complete: function () {
                    removeOverlay(); // Ẩn overlay hoặc loader
                }
            });
        }
    });

    function addOverlay() {
        $('.aside-menu').addClass('dimmed');
    }

    function removeOverlay() {
        $('.aside-menu').removeClass('dimmed');
    }
});
