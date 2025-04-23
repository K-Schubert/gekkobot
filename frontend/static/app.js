const form = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");
const sendButton = form.querySelector("button");

// Focus the input field when the page loads
window.addEventListener("DOMContentLoaded", () => {
  userInput.focus();
});

function addMessage(text, sender) {
  // Create message container
  const messageContainer = document.createElement("div");
  messageContainer.className = sender === "user" ? "message-container user-container" : "message-container bot-container";

  // Create message element
  const msg = document.createElement("div");
  msg.className = `message ${sender}`;

  // Handle markdown-like formatting for bot messages (basic implementation)
  if (sender === "bot") {
    // Convert code blocks
    const formattedText = text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
      .replace(/\*(.*?)\*/g, '<em>$1</em>');           // Italic

    msg.innerHTML = formattedText;
  } else {
    msg.textContent = text;
  }

  // Add message to the container
  messageContainer.appendChild(msg);
  chatBox.appendChild(messageContainer);

  // Scroll to the bottom
  scrollToBottom();

  return msg;
}

function scrollToBottom() {
  chatBox.scrollTop = chatBox.scrollHeight;
}

function createTypingIndicator() {
  const container = document.createElement("div");
  container.className = "message-container bot-container";

  const indicator = document.createElement("div");
  indicator.className = "message bot typing-indicator";

  for (let i = 0; i < 3; i++) {
    const dot = document.createElement("span");
    indicator.appendChild(dot);
  }

  container.appendChild(indicator);
  chatBox.appendChild(container);
  scrollToBottom();

  return container;
}

// Function to handle message submission
function handleSubmit(e) {
  e.preventDefault();
  const message = userInput.value.trim();
  if (!message) return;

  // Disable input and button during processing
  userInput.disabled = true;
  sendButton.disabled = true;

  // Add user message
  addMessage(message, "user");
  userInput.value = "";

  // Create typing indicator
  const typingIndicator = createTypingIndicator();

  fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  })
    .then((res) => {
      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }
      return res.json();
    })
    .then((data) => {
      // Remove typing indicator
      typingIndicator.remove();

      // Add bot response
      addMessage(data.response, "bot");
    })
    .catch((err) => {
      // Remove typing indicator
      typingIndicator.remove();

      // Show error message
      addMessage(`Sorry, I encountered an error: ${err.message}`, "bot");
    })
    .finally(() => {
      // Re-enable input and button
      userInput.disabled = false;
      sendButton.disabled = false;
      userInput.focus();
    });
}

// Attach the submit handler to the form
form.addEventListener("submit", handleSubmit);

// Handle keydown events for enter key
userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    handleSubmit(e);
  }
});
