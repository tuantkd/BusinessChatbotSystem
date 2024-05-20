const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerSendBtn = get(".msger-send-btn");
const msgerChat = get(".msger-chat");
const BOT_IMG = "/static/images/bot_avatar.jpg";
const PERSON_IMG = "/static/icons/user.png";
const BOT_NAME = "BIZGREG";
let senderName = "Guest";
const BOT_MSGS = [];
function markdownToHtml(markdownText) {
    // Tách các dòng văn bản
    const lines = markdownText.trim().split('\n');
    
    let htmlLines = [];
    let inTable = false;

    lines.forEach(line => {
        line = line.trim();

        // Chuyển đổi in đậm
        line = line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

        // Chuyển đổi in nghiêng với dấu gạch dưới
        line = line.replace(/_(.*?)_/g, '<em>$1</em>');

        // Chuyển đổi bảng
        if (line.startsWith('|')) {
            if (!inTable) {
                htmlLines.push('<table>');
                inTable = true;
            }
            const cells = line.split('|').filter(cell => cell.trim() !== '').map(cell => `<td>${cell.trim()}</td>`).join('');
            htmlLines.push(`<tr>${cells}</tr>`);
        } else {
            if (inTable) {
                htmlLines.push('</table>');
                inTable = false;
            }

            // Chuyển đổi danh sách không thứ tự
            if (line.startsWith('- ')) {
                if (!isUlOpen(htmlLines)) {
                    htmlLines.push('<ul>');
                }
                htmlLines.push(`<li>${line.substring(2)}</li>`);
            } else {
                if (isUlOpen(htmlLines)) {
                    htmlLines.push('</ul>');
                }
                htmlLines.push(`<p>${line}</p>`);
            }
        }
    });

    // Đóng thẻ ul nếu còn mở
    if (isUlOpen(htmlLines)) {
        htmlLines.push('</ul>');
    }
    
    // Đóng thẻ table nếu còn mở
    if (inTable) {
        htmlLines.push('</table>');
    }

    return htmlLines.join('\n');
}

function isUlOpen(htmlLines) {
    let ulCount = 0;
    let liCount = 0;

    for (let i = htmlLines.length - 1; i >= 0; i--) {
        if (htmlLines[i].includes('</ul>')) ulCount++;
        if (htmlLines[i].includes('<ul>')) ulCount--;
        if (htmlLines[i].includes('<li>')) liCount++;
        if (htmlLines[i].includes('</li>')) liCount--;

        // Nếu tìm thấy một <ul> mà chưa bị đóng, trả về true
        if (ulCount < 0) return true;
    }

    return false;
}

function getSenderIdFromUrl() {
    const paths = window.location.pathname.split('/');
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

    appendMessage(senderName, PERSON_IMG, "right", msgText);
    callApiChatbot(message);
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

function mergeTextItems(messages) {
    if (!Array.isArray(messages)) return [];
    
    return messages.reduce((acc, current) => {
        if (acc.length === 0) {
            acc.push(current);
        } else {
            const last = acc[acc.length - 1];
            if (last.recipient_id === current.recipient_id && last.hasOwnProperty('text') && current.hasOwnProperty('text')) {
                last.text += ' ' + current.text.trim();
            } else {
                acc.push(current);
            }
        }
        return acc;
    }, []);
}

function callApiChatbot(message) {
    data = {
        "message": message.text,
        "sender": message.senderId
    }
    
    showTypingIndicator();

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
            hideTypingIndicator();
            console.log(res);
            if (res.length === 0) {
                botResponse({text: "Xin lỗi! Tôi chưa hiểu ý của bạn"});
                return;
            }
            messages = mergeTextItems(res);
            messages.forEach(response => {
                botResponse(response);
            });
            var buttons = document.querySelectorAll('input[type="button"]');
            getEventCallApi(buttons);
        },
        error: function (result) {
            hideTypingIndicator();
            console.log(result);
            botResponse({text: "Xin lỗi! Tôi chưa hiểu ý của bạn"});
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

function botResponse(response) {
    if (response.text) {
        responseText = markdownToHtml(response.text);
        appendMessage(BOT_NAME, BOT_IMG, "left", responseText);
    }
    if (response.custom) {
        handleCustomResponse(response.custom);
    }
}

function handleCustomResponse(custom) {
    if (custom.type === "quick_replies") {
        handleQuickReplies(custom.content);
    } 
    // Add other custom response handlers here if needed
}

function handleQuickReplies(content) {
    const { title, buttons } = content;
    const text = markdownToHtml(title);
    const maxButtonsPerPage = 9;
    let buttonsHtml = buttons.map((button, index) => 
        `<input type="button" class="click-btn circle-btn" value="${button.title}" alt="${button.description}" data-description="${button.description}" onclick="sendQuickReply(this)" style="display: ${index < maxButtonsPerPage ? 'inline-block' : 'none'};">`
    ).join('');

    const msgHTML = `
    <div class="msg left-msg">
        <div class="msg-img" style="background-image: url(${BOT_IMG})"></div>
        <div>
            <div class="msg-bubble">
                <div class="msg-info">
                    <div class="msg-info-name">${BOT_NAME}</div>
                    <div class="msg-info-time">${formatDate(new Date())}</div>
                </div>
                <div class="msg-text">
                    ${text}
                </div>
            </div>
            <div class="quick-replies">
                ${buttonsHtml}
                ${buttons.length > maxButtonsPerPage ? '<span class="slide-btn prev-btn" onclick="slideButtons(-1)">&#10094;</span><span class="slide-btn next-btn" onclick="slideButtons(1)">&#10095;</span>' : ''}
            </div>
        </div>
    </div>
    `;

    msgerChat.insertAdjacentHTML("beforeend", msgHTML);
    msgerChat.scrollTop += 500;

    // Initialize tooltips
    document.querySelectorAll('.click-btn').forEach(button => {
        button.addEventListener('mouseenter', function() {
            showTooltip(this, this.getAttribute('data-description'));
        });
        button.addEventListener('mouseleave', hideTooltip);
    });
}

let currentPage = 0;

function slideButtons(direction) {
    const maxButtonsPerPage = 9;
    const buttons = document.querySelectorAll('.quick-replies .click-btn');
    const totalPages = Math.ceil(buttons.length / maxButtonsPerPage);

    currentPage = (currentPage + direction + totalPages) % totalPages;

    buttons.forEach((button, index) => {
        button.style.display = (index >= currentPage * maxButtonsPerPage && index < (currentPage + 1) * maxButtonsPerPage) ? 'inline-block' : 'none';
    });
}

function sendQuickReply(button) {
    const description = button.getAttribute('data-description');
    const message = {
        text: description,
        senderId: senderId
    };
    appendMessage(senderName, PERSON_IMG, "right", description);
    callApiChatbot(message);
}

function get(selector, root = document) {
    return root.querySelector(selector);
}

function showTooltip(element, text) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.innerText = text;
    document.body.appendChild(tooltip);

    const rect = element.getBoundingClientRect();
    tooltip.style.left = `${rect.left + (element.offsetWidth - tooltip.offsetWidth) / 2}px`;
    tooltip.style.top = `${rect.top - tooltip.offsetHeight - 5}px`;
}

function hideTooltip() {
    const tooltip = document.querySelector('.tooltip');
    if (tooltip) {
        tooltip.remove();
    }
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
                console.log("clicked " + this.value);
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

function showTypingIndicator() {
    const typingIndicatorHTML = `
        <div class="msg left-msg typing-indicator">
            <div class="msg-img" style="background-image: url(${BOT_IMG})"></div>
            <div class="msg-bubble">
                <div class="msg-info">
                    <div class="msg-info-name">${BOT_NAME}</div>
                </div>
                <div class="msg-text ellipsis"></div>
            </div>
        </div>
    `;
    msgerChat.insertAdjacentHTML("beforeend", typingIndicatorHTML);
    msgerChat.scrollTop += 500;
}

function hideTypingIndicator() {
    const typingIndicator = document.querySelector('.typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

document.getElementById('logoutButton').addEventListener('click', function() {
    localStorage.removeItem('senderId');
    window.location.href = '/chat';
});