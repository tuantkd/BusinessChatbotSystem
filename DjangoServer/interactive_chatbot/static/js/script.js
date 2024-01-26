const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");

const BOT_MSGS = [];

const BOT_IMG = "static/icons/chat.png";
const PERSON_IMG = "static/icons/user.png";
const BOT_NAME = "BOT";
const PERSON_NAME = "User";

let senderId = localStorage.getItem('senderId');

// If not, create a new one and save it to localStorage
if (!senderId) {
  senderId = 'user-' + Date.now();
  localStorage.setItem('senderId', senderId);
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
    
    appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
    msgerInput.value = "";

    //botResponse();
});


function callApiChatbot(message) {
    data = {
        "message": message.text,
        "session_id": "1234567890",
        "sender": message.senderId
    }
    $.ajax({
        type: "POST",
        contentType: "application/json",
        url: "/chatbot",
        data: JSON.stringify(data),
        dataType: "json",
        success: function(res) {
            console.log(res);
            botResponse(res.data);
        },
        error: function(result) {
            console.log(result);
            botResponse("Sorry, I don't understand");
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
    //const r = random(0, BOT_MSGS.length - 1);
    //const msgText = BOT_MSGS[r];
    //const delay = msgText.split(" ").length * 100;

    setTimeout(() => {
        appendMessage(BOT_NAME, BOT_IMG, "left", msgText);
    }, 100);
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
