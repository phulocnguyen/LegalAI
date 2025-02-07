document.getElementById("send-btn").onclick = sendMessage;

function sendMessage() {
    const messageInput = document.getElementById("message-input");
    const userMessage = messageInput.value.trim();

    if (!userMessage) {
        alert("Please enter a message.");
        return;
    }

    addMessageToChat(userMessage, "user-message");
    messageInput.value = ""; // Xóa nội dung input sau khi gửi

    fetch("/chat_with_ai/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            
        },
        body: JSON.stringify({ question: userMessage }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.answer) {
            addMessageToChat(data.answer, "ai-message");
        } else if (data.error) {
            addMessageToChat(data.error, "error-message");
        }
    })
    .catch(error => {
        addMessageToChat("Lỗi kết nối tới server.", "error-message");
        console.error("Error:", error);
    });
}

function addMessageToChat(message, className) {
    const messageContainer = document.createElement("div");
    messageContainer.className = `message ${className}`;
    messageContainer.textContent = message;

    document.getElementById("messages").appendChild(messageContainer);
}

function getCSRFToken() {
    return document.cookie.split("; ")
        .find(row => row.startsWith("csrftoken"))
        ?.split("=")[1];
}
