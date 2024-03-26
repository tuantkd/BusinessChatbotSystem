$(document).ready(function () {
    const input = $('#regex-values-input');
    const csrftoken = getCookie('csrftoken');
    const baseURL = window.location.origin;
    const pathName = window.location.pathname;
    const currentURL = baseURL + pathName;

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

    function saveRegexVariant(regexValue) {
        const addRegexURL = currentURL + '/add_regex_variant';
        const headers = getHeaders();
        $.ajax({
            url: addRegexURL,
            type: 'POST',
            headers: headers,
            data: JSON.stringify({ regex_value: regexValue }),
            success: function (data) {
                console.log(data);
                addTag(data.pattern, data.id);
            },
            error: function (data) {
                console.log(data);
            }
        });
    }

    $(input).on('keyup', function(e) {
        if (e.key === 'Enter') {
            var tagValue = $(this).val().trim(); // Remove comma and trim whitespace
            // check comma end of the string then remove it
            if (tagValue.charAt(tagValue.length - 1) === ';') {
                tagValue = tagValue.slice(0, -1);
            }
            // check if tag not exist
            const tags = document.querySelectorAll('.tag');
            let tagExist = false;
            for (const tag of tags) {
                if (tag.textContent === tagValue) {
                    tagExist = true;
                    break;
                }
            }
            if (!tagExist) {
                saveRegexVariant(tagValue);
            }

            $(this).val(''); 
        }
    });

    
    function removeRegexVariant(id, tag) {
        
        const removeRegexURL = currentURL + '/remove_regex_variant';
        const headers = getHeaders();
        $.ajax({
            url: removeRegexURL,
            type: 'POST',
            headers: headers,
            data: JSON.stringify({ regex_variant_id: id }),
            success: function (data) {
                let tagsContainer = document.getElementById('regex-values-container');
                tagsContainer.removeChild(tag);
            },
            error: function (data) {
                console.log(data);
            }
        });
    }

    function addTag(text, id) {
        let tagsContainer = document.getElementById('regex-values-container');
        const tag = document.createElement('span');
        tag.className = 'tag';
        tag.textContent = text;
        tag.id = 'tag_' + id;

        const removeBtn = document.createElement('span');
        removeBtn.className = 'remove-tag';
        removeBtn.textContent = 'x';
        removeBtn.id = 'removeBtn_' + text; // Add id to the remove button
        removeBtn.onclick = function() {
            removeRegexVariant(id, tag);
        };

        tag.appendChild(removeBtn);
        tagsContainer.appendChild(tag);
    }

    function init() {
        const element = document.getElementById('regexVariantData');
        const regexVariantData = JSON.parse(element.textContent);
        console.log(regexVariantData);
        for (const regexVariant of regexVariantData) {
            addTag(regexVariant.pattern, regexVariant.id);
        }
    }

    init();
});
