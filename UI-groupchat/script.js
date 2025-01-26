document.getElementById('send-message-btn').addEventListener('click', sendMessage);
document.getElementById('clear-history-btn').addEventListener('click', clearHistory);

// Function to send a message
function sendMessage() {
    const user = document.getElementById('user').value;
    const text = document.getElementById('message-text').value;

    if (!user || !text) {
        alert('Both user name and message text are required.');
        return;
    }

    const messageData = {
        user: user,
        text: text
    };

    fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(messageData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            addMessageToUI(data.message, text);
            document.getElementById('message-text').value = ''; // Clear the message input field
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to clear chat history
function clearHistory() {
    fetch('/clear', {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            document.getElementById('message-list').innerHTML = ''; // Clear the messages from UI
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to add message to the message list
function addMessageToUI(message, text) {
    const messageList = document.getElementById('message-list');
    const messageItem = document.createElement('li');
    messageItem.textContent = `${message.user}: ${text}`;
    messageList.appendChild(messageItem);
}
