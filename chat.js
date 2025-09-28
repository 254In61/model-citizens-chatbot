const sendBtn = document.getElementById('sendBtn');
const userInput = document.getElementById('userInput');
const chatWindow = document.getElementById('chatWindow');
const summaryBtn = document.getElementById('summaryBtn');

let step = 0;
let answers = {};
let botTypingBubble = null;
let userTypingBubble = null;

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keydown', e => {
  if (e.key === 'Enter') sendMessage();
});

userInput.addEventListener('input', () => {
  if (userInput.value.trim() !== '') {
    showUserTyping();
  } else {
    removeUserTyping();
  }
});

function showBotTyping() {
  removeBotTyping();
  botTypingBubble = document.createElement('div');
  botTypingBubble.className = 'typing-bubble bot-typing typing-dots';
  botTypingBubble.innerText = 'Bot is typing...';
  chatWindow.appendChild(botTypingBubble);
  scrollToBottom();
}

function removeBotTyping() {
  if (botTypingBubble) {
    botTypingBubble.remove();
    botTypingBubble = null;
  }
}

function showUserTyping() {
  if (!userTypingBubble) {
    userTypingBubble = document.createElement('div');
    userTypingBubble.className = 'typing-bubble user-typing typing-dots';
    userTypingBubble.innerText = "You're typing...";
    chatWindow.appendChild(userTypingBubble);
    scrollToBottom();
  }
}

function removeUserTyping() {
  if (userTypingBubble) {
    userTypingBubble.remove();
    userTypingBubble = null;
  }
}

function sendMessage() {
  const text = userInput.value.trim();
  if (text === '') return;

  addBubble(text, 'user-bubble');
  userInput.value = '';
  removeUserTyping();

  if (step === 0) {
    answers.full_name = text;
    botReply(`✅ Nice to meet you, ${answers.full_name}! What’s your company name?`);
    step++;
  } else if (step === 1) {
    answers.company_name = text;
    botReply("Awesome! What type of business is it? (e.g., Restaurant, Cafe, Tech Startup)");
    step++;
  } else if (step === 2) {
    answers.business_type = text;
    botReply("Great! How would you describe your brand theme or vibe? (e.g., Modern, Playful, Luxury)");
    step++;
  } else if (step === 3) {
    answers.brand_theme = text;
    botReply("Got it! Do you have any ideas for your logo design? (Or type 'no idea')");
    step++;
  } else if (step === 4) {
    answers.logo_idea = text.toLowerCase().includes("no idea") ? "" : text;
    botReply("Nice! How would you like the interior to feel? (Or type 'skip')");
    step++;
  } else if (step === 5) {
    answers.interior_theme = text.toLowerCase() === "skip" ? "" : text;
    botReply("Do you have any preferred colours for your brand or interior? (Or type 'skip')");
    step++;
  } else if (step === 6) {
    answers.colours = text.toLowerCase() === "skip" ? "" : text;
    botReply("Any specific signage ideas? (Or type 'skip')");
    step++;
  } else if (step === 7) {
    answers.signage = text.toLowerCase() === "skip" ? "" : text;
    botReply("What materials do you prefer? (Or type 'skip')");
    step++;
  } else if (step === 8) {
    answers.materials = text.toLowerCase() === "skip" ? "" : text;
    botReply("What’s your estimated budget in USD?");
    step++;
  } else if (step === 9) {
    answers.budget = parseInt(text.replace(/[^0-9]/g, '')) || 0;
    botReply("Lastly, how many weeks will this project take?");
    step++;
  } else if (step === 10) {
    answers.timeline = parseInt(text.replace(/[^0-9]/g, '')) || 0;

    botReply("✨ Let me prepare your design recommendation... 🤖");
    showBotTyping();

    fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(answers)
    })
      .then(res => res.json())
      .then(data => {
        removeBotTyping();
        botReply(data.reply);

        localStorage.setItem('full_name', answers.full_name);
        localStorage.setItem('company_name', answers.company_name);
        localStorage.setItem('business_type', answers.business_type);
        localStorage.setItem('brand_theme', answers.brand_theme);
        localStorage.setItem('budget', answers.budget);
        localStorage.setItem('timeline', answers.timeline);
        localStorage.setItem('summary', data.reply);

        summaryBtn.style.display = 'block';
      })
      .catch(() => {
        removeBotTyping();
        botReply("⚠️ Oops! Something went wrong. Please try again.");
      });

    step++;
  }

  scrollToBottom();
}

function botReply(message) {
  addBubble(message, 'bot-bubble');
  scrollToBottom();
}

function addBubble(text, className) {
  const bubble = document.createElement('div');
  bubble.className = className;
  bubble.innerText = text;
  chatWindow.appendChild(bubble);
}

function scrollToBottom() {
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

summaryBtn.onclick = () => {
  window.location.href = 'summary.html';
};
