$(document).ready(function () {
    const baseUrl = window.location.origin;
    const pathName = window.location.pathname;
    const currentUrl = `${baseUrl}${pathName}`;
    const csrftoken = getCookie('csrftoken');
    var searchResults = [];

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

    $('.btn-toggle-collapse').click(function () {
        const targetTableId = $(this).closest('.list-group-item').attr('id');
        const storyId = targetTableId.split('_')[2];
        const addStoryTable = $(`#table_story_${storyId}`);
        addStoryTable.toggle('collapse');
        searchItems(storyId);
    });

    function searchItems(storyId) {
        const searchText = $('#searchText-' + storyId).val();
        var itemsList = document.getElementById('items-list-' + storyId);
        itemsList.innerHTML = '';
        const items = searchResults.filter(item => item.text.toLowerCase().includes(searchText.toLowerCase()));
        // Call the search API
        for (const item of items) {
            var itemElement = document.createElement('div');
            itemElement.classList.add('item');

            var textElement = document.createElement('span');
            if (item.type === "intent") {
                textElement.textContent = "Intent: ";
            } else if (item.type === "entity") {
                textElement.textContent = "Entity: ";
            } else if (item.type === "action") {
                textElement.textContent = "Action: ";
            }
            textElement.textContent += item.text;
            textElement.classList.add('search-item');
            textElement.classList.add('search-' + item.type);
            textElement.classList.add('left');
            itemElement.appendChild(textElement);

            var addButton = document.createElement('button');
            addButton.className = "add-story-button";
            var addIcon = document.createElement('i');
            addIcon.className = "fas fa-plus-circle";
            addButton.appendChild(addIcon);

            addButton.addEventListener('click', function () {
                if (item.type === "entity") {
                    addEntity(item.text, storyId);
                }
                else if (item.type === "action") {
                    addAction(item.text, storyId);
                }
                else if (item.type === "intent") {
                    addIntent(item.text, storyId);
                }
                else {
                    addStep(item.type, item.text, storyId);
                }
            });

            itemElement.appendChild(addButton);
            itemsList.appendChild(itemElement);
        }
    }

    $('.search-text').keypress(function (event) {
        const element = $(this).closest('.table-story').attr('id');
        const storyId = element.split('_')[2];
        searchItems(storyId);
    });

    function addStep(type, text, storyId) {
        var storySteps = document.getElementById('story-steps-' + storyId);

        var stepElement = document.createElement('div');
        stepElement.classList.add('step', type);
        stepElement.textContent = text || type.charAt(0).toUpperCase() + type.slice(1);

        var removeBtn = document.createElement('span');
        removeBtn.classList.add('remove-btn');
        removeIcon = document.createElement('i');
        removeIcon.className = 'fas fa-minus-circle';
        removeBtn.appendChild(removeIcon);
        removeBtn.addEventListener('click', function () {
            // If removing an entity, check if it is the last one
            if (type === 'entity' && stepElement.previousElementSibling.classList.contains('entities')) {
                if (!stepElement.nextElementSibling || !stepElement.nextElementSibling.classList.contains('entity')) {
                    storySteps.removeChild(stepElement.previousElementSibling); // Remove the 'entities' label
                }
            }
            storySteps.removeChild(stepElement);
        });

        stepElement.appendChild(removeBtn);
        storySteps.appendChild(stepElement);
    }

    function addEntity(entity_name, storyId) {
        var storySteps = document.getElementById('story-steps-' + storyId);
        var lastStep = storySteps.lastElementChild;
        // Check if the last step is undefined
        if (!lastStep) {
            console.error('Entities must be added after an intent');
            return;
        }
        // Check if the last step is an entity with the same name
        if (lastStep.classList.contains('entity') && lastStep.textContent.trim() === entity_name) {
            console.error('The same entity cannot be added consecutively');
            return;
        }
        if (!lastStep || lastStep.classList.contains('intent')) {
            addStep('entities', 'Entities:', storyId);
        }
        if (lastStep.classList.contains('intent') || lastStep.classList.contains('entities') || lastStep.classList.contains('entity')) {
            addStep('entity', entity_name, storyId);
        }
        else {
            console.error('Entities must be added after an intent');
        }
    }

    function addAction(action_name, storyId) {
        var storySteps = document.getElementById('story-steps-' + storyId);
        var lastStep = storySteps.lastElementChild;
        // Check if the last step is undefined
        if (!lastStep) {
            console.error('Actions must be added after an intent');
            return;
        }
        // Check if the last step is an action with the same name
        if (lastStep.classList.contains('action') && lastStep.textContent.trim() === action_name) {
            console.error('The same action cannot be added consecutively');
            return;
        }
        // Check all previous steps to see if there is an intent before adding an action
        var isIntent = false;
        for (const step of storySteps.children) {
            if (step.classList.contains('intent')) {
                isIntent = true;
            }
        }
        if (isIntent) {
            addStep('action', action_name, storyId);
        } else {
            console.error('Actions must be added after an intent');
        }
    }

    function addIntent(intent_name, storyId) {
        var storySteps = document.getElementById('story-steps-' + storyId);
        var lastStep = storySteps.lastElementChild;
        // Intent không thể theo sau một intent khác
        if (lastStep && lastStep.classList.contains('intent')) {
            console.error('An intent cannot follow another intent');
            return;
        }
        addStep('intent', intent_name, storyId);
    }

    function init() {
        const tableStories = document.getElementsByClassName('table-story');
        for (const tableStory of tableStories) {
            const storyId = tableStory.id.split('_')[2];
            const yamlText = $(`#story-script-${storyId}`).val();
            
            displayYamlTextInStoryTable(yamlText, storyId);
        }
        const searchURL = `${currentUrl}/search`;
        // Call the search API
        $.ajax({
            url: searchURL,
            type: 'POST',
            headers: getHeaders(),
            data: JSON.stringify({}),
            success: function (data) {
                // Handle the search results
                console.log(data);
                var items = data.items;
                searchResults = items;
            },
            error: function (error) {
                // Handle errors
                console.log(error);
            }
        });

    }
    init();

    $('.btn-save-story').click(function (event) {
        event.preventDefault(); // Prevent the form from submitting
        var storyId = $(this).closest('.table-story').attr('id').split('_')[2];
        var storySteps = document.getElementById('story-steps-' + storyId);
        var yamlText = '';

        for (const step of storySteps.children) {
            if (step.classList.contains('intent')) {
                yamlText += `  - intent: ${step.textContent}\n`;
            } else if (step.classList.contains('entities')) {
                yamlText += `    entities:\n`;
            } else if (step.classList.contains('entity')) {
                yamlText += `    - ${step.textContent}\n`;
            } else if (step.classList.contains('action')) {
                yamlText += `  - action: ${step.textContent}\n`;
            }
        }

        const saveStoryStepURL = `${currentUrl}/save_story_step`;
        // Call the save story step API
        const headers = getHeaders();

        $.ajax({
            url: saveStoryStepURL,
            type: 'POST',
            headers: headers,
            data: JSON.stringify({
                story_id: storyId,
                yaml_text: yamlText,
            }),
            success: function (data) {
                // Handle the response
                console.log(data);
                // displayYamlTextInStoryTable(data.yaml_text);
            },
            error: function (error) {
                // Handle errors
                console.log(error);
            }
        });

    });

    function displayYamlTextInStoryTable(yamlText, storyId) {
        // split yamlText into lines
        var lines = yamlText.split('\n');
        var storySteps = document.getElementById('story-steps-' + storyId);
        storySteps.innerHTML = '';
        let intent = '';
        let entity = '';
        let action = '';
        let entitiesFlag = false;
        for (const line of lines) {
            if (line.includes('intent')) {
                intent = line.split(':')[1].trim();
                addStep('intent', intent, storyId);
                entitiesFlag = false;
            } else if (line.includes('entities')) {
                addStep('entities', 'Entities:', storyId);
                entitiesFlag = true;
            } else if (line.includes('action')) {
                action = line.split(':')[1].trim();
                addStep('action', action, storyId);
                entitiesFlag = false;
            } else if (entitiesFlag && line.includes('-')) {
                if (line.includes('-')) {
                    entity = line.split('-')[1].trim();
                    addStep('entity', entity, storyId);
                    entitiesFlag = true;
                }
            }
        }
    }
});