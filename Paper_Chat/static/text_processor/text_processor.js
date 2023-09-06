// Utility function to get selected text from PDF.js viewer
function getSelectedTextFromViewer() {
    console.log("getSelectedTextFromViewer function called.");
    const viewerIframe = document.getElementById('pdf-viewer-frame');
    const viewerDocument = viewerIframe.contentDocument || viewerIframe.contentWindow.document;

    if (viewerDocument) {
        let selectedText = viewerDocument.getSelection();
        let selectedTextData = {
            selected: selectedText.toString(),
            surrounding: selectedText.anchorNode.textContent
        };
        console.log("Surrounding text captured:", selectedTextData.surrounding);
        return selectedTextData;
    }
    return "";
}

function getExpandedSelection(selectedText, surroundingText) {
    const sentences = surroundingText.split('.'); 
    let startIndex = surroundingText.indexOf(selectedText);

    // Try to adjust the start index to the start of the word
    while (startIndex > 0 && /\w/.test(surroundingText[startIndex - 1])) {
        startIndex--;
    }

    let startSentenceIndex = surroundingText.lastIndexOf('.', startIndex) + 1;
    let endSentenceIndex = surroundingText.indexOf('.', startIndex + selectedText.length);
    
    if (endSentenceIndex === -1) {
        endSentenceIndex = surroundingText.length;
    }

    console.log("Sentences split from surrounding text:", sentences);
    console.log("Start index of selected text:", startIndex);
    console.log("Start index of surrounding sentence:", startSentenceIndex);
    console.log("End index of surrounding sentence:", endSentenceIndex);
    return surroundingText.substring(startSentenceIndex, endSentenceIndex).trim();
}

function updateButtonStates() {
    const selectedTextData = getSelectedTextFromViewer();
    const selectedText = selectedTextData.selected;
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
    const textData = getSelectedTextFromViewer();
    const text = textData.selected;
    const count = wordCount(text);

    if (count > 50) {
        sendDataToBackend(text, 'summarize', textData.surrounding);
    } else {
        alert("Please select more than 50 words to summarize.");
    }
}

function explainText() {
    console.log("explainText function called.");
    const textData = getSelectedTextFromViewer();
    const text = textData.selected;
    sendDataToBackend(text, 'explain', textData.surrounding);
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

function sendDataToBackend(text, action, surroundingText) {
    console.log("sendDataToBackend called with action:", action);

    // Use the getExpandedSelection to get an expanded version of the selected text
    const expandedText = getExpandedSelection(text, surroundingText);
    console.log("Expanded text for processing:", expandedText);
    
    console.log("Sending expanded data to backend:", {
        text: expandedText,
        action: action
    });

    // Use the expanded text for both explaining and summarizing in the chat
    if (action === 'explain') {
        appendMessage("user", "Please explain: " + expandedText);
    } else if (action === 'summarize') {
        appendMessage("user", "Please summarize: " + expandedText);
    }

    // Send the expanded text to the backend for processing
    fetch(`/process_text/`, {
        method: 'POST',
        body: JSON.stringify({
            text: expandedText,
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
