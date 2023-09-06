// Utility function to get selected text from PDF.js viewer
function getSelectedTextFromViewer() {
    console.log("getSelectedTextFromViewer function called.");
    const viewerIframe = document.getElementById('pdf-viewer-frame');
    const viewerDocument = viewerIframe.contentDocument || viewerIframe.contentWindow.document;

    if (viewerDocument) {
        let selection = viewerDocument.getSelection();
        if (!selection.rangeCount) return "";
        let range = selection.getRangeAt(0).cloneRange();  // Get the first selected range

        const MAX_EXPANSION = 500; // Define a limit to avoid infinite loops
        let expansions = 0;

        // Expand the range to capture more context
        while (range.startOffset > 0 && expansions < MAX_EXPANSION) {
            range.setStart(range.startContainer, range.startOffset - 1);
            expansions++;
        }
        while (range.endOffset < (range.endContainer.textContent.length - 1) && expansions < MAX_EXPANSION) {
            range.setEnd(range.endContainer, range.endOffset + 1);
            expansions++;
        }

        const surrounding = range.toString();
        console.log("Surrounding text captured:", surrounding);
        return {
            selected: selection.toString(),
            surrounding: surrounding
        };
    }
    return "";
}

function getExpandedSelection(selectedText, surroundingText) {
    let startIndex = surroundingText.indexOf(selectedText);
    let startSentenceIndex = startIndex;
    let endSentenceIndex = startIndex + selectedText.length;
    
    // Expand to the start of the word
    while (startSentenceIndex > 0 && !/\s/.test(surroundingText[startSentenceIndex])) {
        startSentenceIndex--;
    }

    // Expand to the end of the word
    while (endSentenceIndex < surroundingText.length && !/\s/.test(surroundingText[endSentenceIndex])) {
        endSentenceIndex++;
    }

    // Attempt to expand to the start of the sentence
    let sentenceStartIndex = surroundingText.lastIndexOf('.', startSentenceIndex) + 1;
    if (sentenceStartIndex > 0 && sentenceStartIndex < startIndex) {
        startSentenceIndex = sentenceStartIndex;
    }

    // Attempt to expand to the end of the sentence
    let sentenceEndIndex = surroundingText.indexOf('.', endSentenceIndex);
    if (sentenceEndIndex === -1) {
        sentenceEndIndex = surroundingText.length;
    }
    if (sentenceEndIndex > endSentenceIndex) {
        endSentenceIndex = sentenceEndIndex;
    }

    console.log("Sentences split from surrounding text:", surroundingText.split('.'));
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

    // Use the getExpandedSelection to get an expanded version of the selected text only for 'explain' action
    let processedText = action === 'explain' ? getExpandedSelection(text, surroundingText) : text;
    console.log("Processed text for sending to backend:", processedText);
    
    console.log("Sending processed data to backend:", {
        text: processedText,
        action: action
    });

    // Use the processed text for both explaining and summarizing in the chat
    if (action === 'explain') {
        appendMessage("user", "Please explain: " + processedText);
    } else if (action === 'summarize') {
        appendMessage("user", "Please summarize: " + processedText);
    }

    // Send the processed text to the backend for processing
    fetch(`/process_text/`, {
        method: 'POST',
        body: JSON.stringify({
            text: processedText,
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
