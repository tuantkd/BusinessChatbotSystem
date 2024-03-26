$(document).ready(function () {
    const input = $('#tags-input');
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

    function saveSynonymVariant(synonymValue) {
        const addSynonymURL = currentURL + '/add_synonym_variant';
        const headers = getHeaders();
        $.ajax({
            url: addSynonymURL,
            type: 'POST',
            headers: headers,
            data: JSON.stringify({ synonym_value: synonymValue }),
            success: function (data) {
                console.log(data);
                addTag(data.synonym_value, data.id);
            },
            error: function (data) {
                console.log(data);
            }
        });
    }

    $(input).on('keyup', function(e) {
        if (e.key === ';' || e.key === 'Enter') {
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
                saveSynonymVariant(tagValue);
            }

            $(this).val(''); 
        }
    });

    
    function removeSynonymVariant(id, tag) {
        
        const removeSynonymURL = currentURL + '/remove_synonym_variant';
        const headers = getHeaders();
        $.ajax({
            url: removeSynonymURL,
            type: 'POST',
            headers: headers,
            data: JSON.stringify({ synonym_variant_id: id }),
            success: function (data) {
                let tagsContainer = document.getElementById('tags-container');
                tagsContainer.removeChild(tag);
            },
            error: function (data) {
                console.log(data);
            }
        });
    }

    function addTag(text, id) {
        let tagsContainer = document.getElementById('tags-container');
        const tag = document.createElement('span');
        tag.className = 'tag';
        tag.textContent = text;
        tag.id = 'tag_' + id;

        const removeBtn = document.createElement('span');
        removeBtn.className = 'remove-tag';
        removeBtn.textContent = 'x';
        removeBtn.id = 'removeBtn_' + text; // Add id to the remove button
        removeBtn.onclick = function() {
            removeSynonymVariant(id, tag);
        };

        tag.appendChild(removeBtn);
        tagsContainer.appendChild(tag);
    }

    function init() {
        const element = document.getElementById('synonymVariantData');
        const synonymVariantData = JSON.parse(element.textContent);
        console.log(synonymVariantData);
        for (const synonymVariant of synonymVariantData) {
            addTag(synonymVariant.synonym_value, synonymVariant.id);
        }
    }

    init();
});
