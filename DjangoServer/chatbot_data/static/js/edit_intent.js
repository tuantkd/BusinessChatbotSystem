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

    addExpression = () => {
        expressionText = $('#text').val();
        let addUrl = `${currentUrl}/expression/add`;
        const headers = getHeaders();

        $.ajax({
            url: addUrl,
            type: 'POST',
            headers: headers,
            data: JSON.stringify({ expression_text: expressionText }),
            success: (res) => {
                window.location.reload();
            },
            error: (xhr, errmsg, err) => {
                console.log(errmsg);
            }
        });
    }

    $('#addExpressionForm').submit((e) => {
        e.preventDefault();
        addExpression();
    })

    $('.delete-expression').click(function () {
        const expressionSpan = $(this).closest('.list-group-item').find('span[id^="expression_"]');
        const expressionId = expressionSpan.attr('id').split('_')[1];
        const deleteUrl = `${currentUrl}/delete_expression/${expressionId}`
        const headers = getHeaders();

        $.ajax({
            url: deleteUrl,
            type: 'POST',
            headers: headers,
            data: {
                expression_id: expressionId
            },
            success: function (response) {
                console.log(response.message);
                window.location.reload();
            },
            error: function (xhr, errmsg, err) {
                console.log(errmsg);
            }
        });
    });

    $(document).on('mouseup keyup', function (e) {
        // Lặp qua từng .list-group-item để xử lý riêng lẻ
        $('.list-group-item').each(function () {
            const $listGroupItem = $(this); // Lưu tham chiếu đến list-group-item hiện tại
            let selectedText = window.getSelection().toString();
            const $linkButton = $listGroupItem.find('.btn-outline-secondary.link-btn'); // Tìm button link trong list-group-item này

            if (selectedText.length > 0) {
                // Kiểm tra xem text được highlight có nằm trong list-group-item này không
                const isTextInItem = window.getSelection().anchorNode.parentNode === $listGroupItem.find('span[id^="expression_"]')[0];
                if (isTextInItem) {
                    // Enable button nếu có text được highlight trong list-group-item này
                    $linkButton.removeClass('disabled').removeAttr('disabled');
                } else {
                    // Ngược lại, disable button nếu text được highlight không nằm trong list-group-item này
                    $linkButton.addClass('disabled').attr('disabled', 'disabled');
                }
            } else {
                // Disable button nếu không có text được highlight
                $linkButton.addClass('disabled').attr('disabled', 'disabled');
            }
        });
    });
    
    function getSelectionCharacterOffsetWithin(element) {
        var start = 0;
        var end = 0;
        var doc = element.ownerDocument || element.document;
        var win = doc.defaultView || doc.parentWindow;
        var sel;
        if (typeof win.getSelection != "undefined") {
            sel = win.getSelection();
            if (sel.rangeCount > 0) {
                var range = win.getSelection().getRangeAt(0);
                var selectedText = range.toString(); // Lấy text được chọn
    
                // Lưu ý số lượng ký tự bị loại bỏ ở đầu chuỗi
                var trimmedStartLength = selectedText.length - selectedText.trimStart().length;
    
                var preCaretRange = range.cloneRange();
                preCaretRange.selectNodeContents(element);
                preCaretRange.setEnd(range.startContainer, range.startOffset);
                start = preCaretRange.toString().length - trimmedStartLength; // Cập nhật start bằng cách trừ đi số ký tự bị loại bỏ
                end = start + selectedText.trim().length; // Sử dụng độ dài của chuỗi đã trim để tính toán end
            }
        } else if ((sel = doc.selection) && sel.type != "Control") {
            // Đối với IE, bạn cũng sẽ cần xử lý tương tự như trên, nhưng code này giả sử rằng bạn không sử dụng IE.
        }
        return { start: start, end: end };
    }    

    $('.list-group').on('click', '.link-btn:not(.disabled)', function() {
        const expressionSpan = $(this).closest('.list-group-item').find('span[id^="expression_"]');
        const expressionId = expressionSpan.attr('id').split('_')[1];
        let selectedText = window.getSelection().toString();
        const elementText = document.getElementById('expression_' + expressionId);
        const selectionOffsets = getSelectionCharacterOffsetWithin(elementText);

        const parameterStart = selectionOffsets.start;
        const parameterEnd = selectionOffsets.end;
        const addParameterUrl = `${currentUrl}/expression/${expressionId}/parameter/add`;
        const headers = getHeaders();
        if (selectedText.length > 0 && expressionId) {
            const data = {
                parameter_start: parameterStart,
                parameter_end: parameterEnd,
                parameter_value: selectedText,
            };
            $.ajax({
                url: addParameterUrl,
                type: 'POST',
                headers, headers,
                data: JSON.stringify(data),
                contentType: 'application/json',
                success: function(response) {
                    console.log('Parameter created successfully', response);
                    window.location.reload();
                },
                error: function(error) {
                    console.error('Error creating parameter', error);
                }
            });
        }
    });

    $('.list-group').on('click', 'button[data-toggle="collapse"]', function(event) {
        event.preventDefault();
        const targetSelector = $(this).attr('data-target');
        $(targetSelector).toggle('collapse');

        const icon = $(this).find('.fa');
        if (icon.hasClass('fa-arrow-down')) {
            icon.removeClass('fa-arrow-down').addClass('fa-arrow-up');
        } else {
            icon.removeClass('fa-arrow-up').addClass('fa-arrow-down');
        }
    });

    $('.entity-select').change(function() {
        var saveButton = $(this).closest('tr').find('.save-btn');
        
        if ($(this).val() === "") {
            saveButton.prop('disabled', true);
            saveButton.addClass('disabled');
        } else {
            saveButton.prop('disabled', false);
            saveButton.removeClass('disabled');
        }
    });

    $('.save-btn').click(function(event) {
        event.preventDefault();
        const parameterId = $(this).closest('tr').attr('data-parameter-id');
        const entityId = $(this).closest('tr').find('.entity-select').val();
        const updateParameterUrl = `${currentUrl}/parameter/${parameterId}/update`;
        const headers = getHeaders();
        const data = {
            entity_id: entityId,
        };

        const self = this;
        $.ajax({
            url: updateParameterUrl,
            type: 'POST',
            headers: headers,
            data: JSON.stringify(data),
            success: function(response) {
                console.log('Saved successfully');
                $(self).prop('disabled', true);
                $(self).addClass('disabled');
            },
            error: function(error) {
                console.error('Error saving');
            }
        });
    });

    $('.delete-btn').click(function(event) {
        event.preventDefault();
        const parameterId = $(this).closest('tr').attr('data-parameter-id');
        const deleteParameterUrl = `${currentUrl}/parameter/${parameterId}/delete`;
        const headers = getHeaders();

        if (confirm('Are you sure you want to delete this parameter?')) {
            $.ajax({
                url: deleteParameterUrl,
                type: 'POST',
                headers: headers,
                success: function(response) {
                    console.log('Deleted successfully');
                    // remove row
                    window.location.reload();

                },
                error: function(error) {
                    console.error('Error deleting');
                }
            });
        }
    });

    $('.send-expression').click(function(event) {
        event.preventDefault();
        if (!confirm("Are you sure you want to send this expression to the RASA server?")) {
        }
        const expressionSpan = $(this).closest('.list-group-item').find('span[id^="expression_"]');
        const expressionId = expressionSpan.attr('id').split('_')[1];
        const predictExpressionUrl = `${currentUrl}/expression/${expressionId}/predict`;
        var expressionText = $('#expression_'+expressionId).text();
        const headers = getHeaders();
        $.ajax({
            url: predictExpressionUrl,
            type: 'POST',
            headers: headers,
            contentType: 'application/json',
            data: JSON.stringify({ expression_text : expressionText }),
            success: function(response) {
                console.log(response);
                window.location.reload();
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    });

    function init () {
        const parameterDataElement = document.getElementById('parameterListData');
        const parameterList = JSON.parse(parameterDataElement.textContent);
        parameterList.forEach((parameter) => {
            const expressionElement = document.getElementById(`expression_${parameter.expression}`);
            if (expressionElement) {
                const regex = new RegExp(`(${parameter.parameter_value})`, 'gi');
                const newText = expressionElement.innerHTML.replace(regex, `<mark title="${parameter.entity_name}">$1</mark>`);
                expressionElement.innerHTML = newText;
            }
        });
    
    }
    init();
});
