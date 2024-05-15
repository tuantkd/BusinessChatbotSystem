const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerSendBtn = get(".msger-send-btn");
const msgerChat = get(".msger-chat");
const BOT_IMG = "/static/images/bot_avatar.jpg";
const PERSON_IMG = "/static/icons/user.png";
const BOT_NAME = "BIZGREG";
let  senderName = "Guest";
const BOT_MSGS = [];

function getSenderIdFromUrl() {
    const paths  = window.location.pathname.split('/');
    if (paths.length > 2) {
        return paths[2];
    }
    return null;
}

function getSenderIdFromLocalStorage() {
    return localStorage.getItem('senderId');
}

// If not, create a new one and save it to localStorage
function get_user() {
    senderId = getSenderIdFromUrl();
    if (senderId === null || senderId === "") {
        senderId = getSenderIdFromLocalStorage();
        if (senderId !== null && senderId !== "") {
            // navigate to the new url
            window.location.replace(`/chat/${senderId}`);
        }
        else {
            // clear the local storage
            localStorage.clear();
            return;
        }
    }
    else {
        localStorage.setItem('senderId', senderId);
    } 

    csrf_token = getCookie('csrftoken');
    fetch(`/chat/get_current_user/${senderId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        }
    })
    .then(response => response.json())
    .then(data => {
        senderName = data['senderName'];
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

get_user();

function enableSubmitButton() {
    const nameInput = document.getElementById("nameInput");
    const submitButton = document.getElementById("submitButton");
    if (nameInput.value !== "") {
        submitButton.disabled = false;
    } else {
        submitButton.disabled = true;
    }
}

msgerForm.addEventListener("submit", event => {
    event.preventDefault();

    const msgText = msgerInput.value;
    if (!msgText) return;

    const message = {
        text: msgText,
        senderId: senderId
    };

    callApiChatbot(message);

    appendMessage(senderName, PERSON_IMG, "right", msgText);
    msgerInput.value = "";
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function callApiChatbot(message) {
    data = {
        "message": message.text,
        "sender": message.senderId
    }

    $.ajax({
        type: "POST",
        contentType: "application/json",
        url: "/chat/",
        data: JSON.stringify(data),
        dataType: "json",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        success: function (res) {
            console.log(res);
            botResponse(res.text);
            var buttons = document.querySelectorAll('input[type="button"]');
            getEventCallApi(buttons);
        },
        error: function (result) {
            console.log(result);
            botResponse("Xin lỗi! Tôi chưa hiểu ý của bạn");
        }
    });
}

function appendMessage(name, img, side, text) {
    const msgHTML = `
        <div class="msg ${side}-msg">
            <div class="msg-img" style="background-image: url(${img})"></div>
            <div class="msg-bubble">
                <div class="msg-info">
                    <div class="msg-info-name">${name}</div>
                    <div class="msg-info-time">${formatDate(new Date())}</div>
                </div>
                <div class="msg-text">${text}</div>
            </div>
        </div>
    `;

    msgerChat.insertAdjacentHTML("beforeend", msgHTML);
    msgerChat.scrollTop += 500;
}

function botResponse(msgText) {
    const isBusinessTypes = msgText.indexOf("business_types=");
    const isBusinessTypeStatus = msgText.indexOf("type_of_business=");
    if (isBusinessTypes !== -1) {
        handleGenBtn(msgText, "business_types=", "Vui lòng chọn loại hình để biết thêm thông tin");
    } else if (isBusinessTypeStatus !== -1) {
        handleGenBtn(msgText, "type_of_business=", "Vui lòng chọn trạng thái để biết thêm thông tin");
    } else {
        appendMessage(BOT_NAME, BOT_IMG, "left", msgText);
    }
}

function handleGenBtn(textResponse, key, text_more) {
    textFull = textResponse.split(key);
    btnList = textFull[0];
    textSingles = textFull[1].split(',');
    var key = 0;
    for (const textMes of textSingles) {
        btnList += '<input type="button" class="click-btn" id="button_' + (key++) + '" value="' + textMes.trim() + '">';
    }
    btnList += "<br>" + text_more;
    appendMessage(BOT_NAME, BOT_IMG, "left", btnList);
    disableInputAndBtnSendChatbot(msgerInput, msgerSendBtn, true);
}

function get(selector, root = document) {
    return root.querySelector(selector);
}

function formatDate(date) {
    const h = "0" + date.getHours();
    const m = "0" + date.getMinutes();

    return `${h.slice(-2)}:${m.slice(-2)}`;
}

function random(min, max) {
    return Math.floor(Math.random() * (max - min) + min);
}

function getEventCallApi(buttons) {
    for (var i = 0; i < buttons.length; i++) {
        if (buttons[i].type === 'button') {
            buttons[i].addEventListener('click', function() {
                console.log(this.value);
                const message = {
                    text: this.value,
                    senderId: senderId
                };
                callApiChatbot(message);
                appendMessage(senderName, PERSON_IMG, "right", this.value);
                disableAllInputButtons(buttons);
                disableInputAndBtnSendChatbot(msgerInput, msgerSendBtn, false);
            });
        }
    }
}

function disableAllInputButtons(buttons) {
    for (var i = 0; i < buttons.length; i++) {
        if (buttons[i].type === 'button') {
            buttons[i].disabled = true;
        }
    }
}

function disableInputAndBtnSendChatbot(eleInput, eleBtn, isDisable) {
    eleInput.disabled = isDisable;
    eleBtn.disabled = isDisable;
}
