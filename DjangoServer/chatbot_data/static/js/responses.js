$(document).ready(function() {
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
    selectBot.addEventListener('change', function() {
        // Lấy option được chọn
        var selectedOption = selectBot.options[selectBot.selectedIndex];
        // Cập nhật nội dung của span
        selectedBotNameSpan.textContent = selectedOption.textContent;
    });

});