// Toggle Chat Visibility
function toggleChat() {
  const chatWindow = document.getElementById("chatWindow");
  chatWindow.classList.toggle("active");
}

function handleKeyPress(event) {
  if (event.key === "Enter") {
    sendMessage();
  }
}

function appendMessage(text, sender) {
  const chatBody = document.getElementById("chatBody");
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", sender);
  msgDiv.textContent = text;
  chatBody.appendChild(msgDiv);
  chatBody.scrollTop = chatBody.scrollHeight;
  return msgDiv;
}

async function sendMessage() {
  const input = document.getElementById("userInput");
  const sendBtn = document.getElementById("sendBtn");
  const text = input.value.trim();

  if (!text) return;

  appendMessage(text, "user");
  input.value = "";
  input.disabled = true;
  sendBtn.disabled = true;

  const loadingMsg = appendMessage("Thinking...", "bot");

  try {
    // Send request to your Flask backend endpoint
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });

    const data = await response.json();

    if (response.ok) {
      loadingMsg.textContent = data.reply;
    } else {
      loadingMsg.textContent = "Error: " + (data.error || "Failed to fetch response.");
      loadingMsg.classList.add("error");
    }
  } catch (err) {
    loadingMsg.textContent = "Error: Unable to connect to server.";
    loadingMsg.classList.add("error");
  } finally {
    input.disabled = false;
    sendBtn.disabled = false;
    input.focus();
  }
}

// Draggable Window Feature (Click and hold the header to drag)
document.addEventListener("DOMContentLoaded", () => {
  const chatWindow = document.getElementById("chatWindow");
  
  if (!chatWindow) return;

  const header = chatWindow.querySelector(".chatbot-header");
  let isDragging = false;
  let offsetX = 0;
  let offsetY = 0;

  header.addEventListener("mousedown", (e) => {
    // Prevent dragging when clicking the close button
    if (e.target.classList.contains("chatbot-close")) return;

    isDragging = true;
    const rect = chatWindow.getBoundingClientRect();

    offsetX = e.clientX - rect.left;
    offsetY = e.clientY - rect.top;

    // Convert CSS layout properties to absolute pixels on drag start
    chatWindow.style.bottom = "auto";
    chatWindow.style.right = "auto";
    chatWindow.style.left = `${rect.left}px`;
    chatWindow.style.top = `${rect.top}px`;

    document.addEventListener("mousemove", onMouseMove);
    document.addEventListener("mouseup", onMouseUp);
  });

  function onMouseMove(e) {
    if (!isDragging) return;

    let newLeft = e.clientX - offsetX;
    let newTop = e.clientY - offsetY;

    // Keep chat window inside viewport boundaries
    const maxX = window.innerWidth - chatWindow.offsetWidth;
    const maxY = window.innerHeight - chatWindow.offsetHeight;

    newLeft = Math.max(0, Math.min(newLeft, maxX));
    newTop = Math.max(0, Math.min(newTop, maxY));

    chatWindow.style.left = `${newLeft}px`;
    chatWindow.style.top = `${newTop}px`;
  }

  function onMouseUp() {
    isDragging = false;
    document.removeEventListener("mousemove", onMouseMove);
    document.removeEventListener("mouseup", onMouseUp);
  }

  const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

fetch('/api/chat', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken  // Pass token here
    },
    body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        if (data.reply) {
            // Display reply
        } else {
            // Display error
        }
    })
    .catch(err => console.error(err));

  function changeSize(delta) {
    const chatWin = document.querySelector('.chat-window');
    
    let currentWidth = chatWin.offsetWidth;
    let currentHeight = chatWin.offsetHeight;

    // Apply new dimensions within limits
    chatWin.style.width = Math.min(Math.max(currentWidth + delta, 300), 800) + 'px';
    chatWin.style.height = Math.min(Math.max(currentHeight + delta, 400), 800) + 'px';
  } 
});