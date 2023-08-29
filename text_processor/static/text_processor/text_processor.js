// Utility function to get selected text from PDF.js viewer
function getSelectedTextFromViewer() {
    const viewerIframe = document.getElementById('pdf-viewer-frame');
    const viewerDocument = viewerIframe.contentDocument || viewerIframe.contentWindow.document;

    if (viewerDocument) {
        return viewerDocument.getSelection().toString();
    }

    return "";
}

function updateButtonStates() {
    const selectedText = getSelectedTextFromViewer();
    const summarizeBtn = parent.document.getElementById('summarizeBtn');
    const explainBtn = parent.document.getElementById('explainBtn');
    const optionsDiv = parent.document.getElementById('text-options');

    if (selectedText.trim() !== "") {
        summarizeBtn.disabled = false;
        explainBtn.disabled = false;
        optionsDiv.style.display = 'block';
    } else {
        summarizeBtn.disabled = true;
        explainBtn.disabled = true;
        optionsDiv.style.display = 'none';
    }
}

function wordCount(str) {
    return str.split(/\s+/).filter(Boolean).length;
}

function summarizeText() {
    console.log("summarizeText function called.");
    const text = getSelectedTextFromViewer();
    const count = wordCount(text);

    if (count > 50) {
        sendDataToBackend(text, 'summarize');
    } else {
        alert("Please select more than 50 words to summarize.");
    }
}

function explainText() {
    console.log("explainText function called.");
    const text = getSelectedTextFromViewer();
    sendDataToBackend(text, 'explain');
}

function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    appendMessage("user", userInput);

    const pdfContent = document.getElementById("pdf-content").value;

    const data = {
        text: userInput,
        action: "summarize",
        pdf_content: pdfContent
    };

    fetch("/process_text/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        appendMessage("bot", data.result);
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

function sendDataToBackend(text, action) {
    console.log("sendDataToBackend called with action:", action);
    if (action === 'explain') {
        appendMessage("user", "Please explain: " + text);
    } else if (action === 'summarize') {
        appendMessage("user", "Please summarize: " + text);
    }

    fetch(`/process_text/`, {
        method: 'POST',
        body: JSON.stringify({
            text: text,
            action: action
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("Received response from server:", data);
        appendMessage("bot", data.result);
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error.message);
    });
}

function appendMessage(sender, message) {
    console.log(`Appending message from ${sender}: ${message}`);
    const chatMessages = document.getElementById("chat-messages");
    const messageDiv = document.createElement("div");
    messageDiv.className = sender + "-message";
    const messageContent = `
        <span class="message-label">${sender === "user" ? "You" : "Bot"}:</span>
        <p class="message-content">${message}</p>
    `;
    messageDiv.innerHTML = messageContent;
    chatMessages.appendChild(messageDiv);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.getElementById('pdf-upload-input').addEventListener('change', function(event) {
    var file = event.target.files[0];
    if (file) {
        var reader = new FileReader();
        reader.onload = function(evt) {
            var blob = new Blob([evt.target.result], {type: 'application/pdf'});
            var blobURL = URL.createObjectURL(blob);
            document.getElementById('pdf-viewer-frame').src = '{% static "pdfjs-3/web/viewer.html" %}?file=' + encodeURIComponent(blobURL);
        };
        reader.readAsArrayBuffer(file);
    }
});

function bindIframeEvents() {
    const pdfViewerFrame = document.getElementById('pdf-viewer-frame');
    if (pdfViewerFrame) {
        console.log("Iframe loaded");

        pdfViewerFrame.contentWindow.document.addEventListener('mouseup', function() {
            console.log("Mouseup event triggered inside iframe");
            updateButtonStates();
        });
    } else {
        setTimeout(bindIframeEvents, 500);  // retry after 500ms
    }
}
document.addEventListener("DOMContentLoaded", bindIframeEvents);
