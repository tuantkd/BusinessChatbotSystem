$(document).ready(function () {
    const intentId = window.location.pathname.split('/')[4];

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
    
    function addExpression() {
        const newObj = {};
        newObj.expression_text = document.getElementById('text').value;
        let currentPath = window.location.pathname;
        let url = `${currentPath}/expression/add`;
        const csrftoken = getCookie('csrftoken'); // Get CSRF token from cookies
    
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken, // Include CSRF token in the request header
            },
            body: JSON.stringify(newObj),
        })
        .then(response => response.text()) // change this line
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    document.getElementById('addExpressionForm').addEventListener('submit', function (event) {
        event.preventDefault();
    });

    document.getElementById('text').addEventListener('keyup', function (event) {
        if (event.key === 'Enter') {
            addExpression();
        }
    });
});
