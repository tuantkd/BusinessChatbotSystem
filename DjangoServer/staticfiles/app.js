class Chatbox {
    constructor() {
        this.args = {
            // openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button'),
            btnUploadImage: document.querySelector('.btn-upload-image'),
            inputs: document.querySelectorAll('input[type=file]')
        }

        this.state = false;
        this.messages = [];
    }

    // Hiển thị chatbox khi click vào nút chat
    display() {
        const {openButton, chatBox, sendButton, btnUploadImage, inputs} = this.args;

        // openButton.addEventListener('click', () => this.toggleState(chatBox))

        sendButton.addEventListener('click', () => this.onSendButton(chatBox, inputs, false))

        btnUploadImage.addEventListener('click', () => this.onSendButton(chatBox, inputs, true))

        const node = chatBox.querySelector('input');

        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
    }

    toggleState(chatbox) {
        this.state = !this.state;
        if(this.state) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

   
    onSendButton(chatbox, fileInput, isFile) {
        var textField = chatbox.querySelector('input');
        let textQuestion = textField.value
        const formData = new FormData();

        if ((fileInput && isFile) || textQuestion !== "") {
            const file = fileInput ? fileInput[0]?.files[0] : { name: "" };
            formData.append('file_image', file);
            this.messages.push({ 
                name: "User",
                message: {
                    "answer": "",
                    "filename_upload": file.name,
                    "result_files": []
                } 
            });

            formData.append('message', textQuestion);
            this.messages.push({ 
                name: "User",
                message: {
                    "answer": textQuestion,
                    "filename_upload": "",
                    "result_files": []
                } 
            });
        } else {
            return;
        }

        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: formData,
            mode: 'cors',
        })
        .then(response => response.json())
        .then((data) => {
            let result = data.answer.localeCompare("");
            if (result !== 0) {
                let msg2 = { name: "Sam", message: data };
                this.messages.push(msg2);
                this.updateChatImage(chatbox);
                textField.value = '';
            } else {
                let msg = { name: "Image", message: data };
                this.messages.push(msg);
                this.updateChatImage(chatbox);
            }
        }).catch((error) => {
            console.error('Error:', error);
            textField.value = '';
        });
    }

 
    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {
            if (item.name === "Sam")
            {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
            }
            else
            {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
        });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }

    updateChatImage(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {
            if (item.message.answer !== "") {
                if (item.name === "Sam") {
                    html += '<div class="messages__item messages__item--visitor">' + item.message.answer + '</div>';
                } else {
                    html += '<div class="messages__item messages__item--operator">' + item.message.answer + '</div>'
                }
            }
            var images = "";
            for(const image of item.message.result_files){
                images += '<div class="image-wrap"><div class="image-frame">' +
                            '<img src="' + image + '" alt="image-result">' +
                        '</div></div>';
            }
            if (item.name === "Image") {
        
                let imageData = '';
                for (const image of item.message.result_files) {
                    imageData += '<div class="image-frame"><img src="' + image + '" alt="image"></div>';
                }

                html += '<div class="messages__item messages__item--visitor">' +
                            '<p>Các mẫu được gợi ý dưới đây:</>' +
                            '<div class="image-wrap">' + imageData + '</div>' + 
                        '</div>';

                html += '<div class="messages__item messages__item--operator">' +
                            '<div class="image-wrap">' +
                                '<div class="image-frame">' +
                                    '<img src="' + '/static/uploads/' + item.message.filename_upload + '" alt="image-upload">' +
                                '</div>' +
                            '</div>' +
                        '</div>';
            }
        });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }

    // onUploadImage(fileInput, chatbox) {
    //     if (fileInput[0].files.length === 0) {
    //         Swal.fire({
    //             icon: 'error',
    //             title: 'Lỗi',
    //             text: 'Hình ảnh chưa được tải lên'
    //         })
    //     }

    //     const file = fileInput[0].files[0];
    //     const formData = new FormData();
    //     formData.append('file_image', file);
        
    //     fetch('http://127.0.0.1:5000/upload-image', {
    //         method: 'POST',
    //         mode: 'cors',
    //         body: formData
    //     })
    //     .then(response => response.json())
    //     .then((data) => {
    //         console.log(data);
    //         let msg = { name: "Image", message: data };
    //         this.messages.push(msg);
    //         this.updateChatImage(chatbox);
    //     })
    //     .catch((error) => {
    //         console.error('Error uploading file:', error);
    //     });
    // }
}

const chatbox = new Chatbox();
chatbox.display();