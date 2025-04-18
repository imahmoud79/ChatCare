document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('message-form');
    const input = document.getElementById('message-input');
    const messagesContainer = document.getElementById('chat-messages');

    // Scroll to bottom of messages on page load
    scrollToBottom();

    // Handle form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        const message = input.value.trim();
        if (!message) return;

        // Disable input and button while sending
        const submitButton = form.querySelector('button[type="submit"]');
        input.disabled = true;
        submitButton.disabled = true;

        // Clear input
        input.value = '';

        try {
            const response = await fetch('/chat/send/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();
            
            if (data.status === 'success') {
                // Add user message
                appendMessage(data.user_message, false);
                
                // Add bot response
                appendMessage(data.message, true);
            } else {
                console.error('Error:', data.message);
                appendMessage('Sorry, there was an error processing your message.', true);
            }
        } catch (error) {
            console.error('Error:', error);
            appendMessage('Sorry, there was an error sending your message.', true);
        } finally {
            // Re-enable input and button
            input.disabled = false;
            submitButton.disabled = false;
            input.focus();
        }
    });

    // Function to append a new message
    function appendMessage(content, isBot) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isBot ? 'counselor' : 'user'}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = content.replace(/\n/g, '<br>');
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        const timeSpan = document.createElement('small');
        timeSpan.className = 'text-muted';
        timeSpan.textContent = new Date().toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
        timeDiv.appendChild(timeSpan);
        
        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timeDiv);
        messagesContainer.appendChild(messageDiv);
        
        scrollToBottom();
    }

    // Function to scroll to bottom of messages
    function scrollToBottom() {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // Handle textarea auto-resize and enter key
    input.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            form.dispatchEvent(new Event('submit'));
        }
    });

    // Function to get CSRF token from cookies
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
}); 