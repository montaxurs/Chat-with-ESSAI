css = '''
<style>
.chat-container {
    max-width: 500px;
    margin: 0 auto;
    padding: 1rem;
    background-color: #343541;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

/* Common styles for both bot and user messages */
.chat-message {
    padding: 0.75rem;
    border-radius: 2.5rem;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: flex-start;
    max-width: 75%;
}

/* User message on the left */
.chat-message.user {
    background-color: #2b313e;
    flex-direction: row;
    margin-left: 0;
    margin-right: auto;
    align-items: center;
}

/* Bot message on the right */
.chat-message.bot {
    background-color: #475063;
    flex-direction: row-reverse;
    margin-left: auto;
    margin-right: 0;
}

.chat-message .avatar {
    width: 15%; /* Adjusted for better spacing */
    align-self: flex-start;
}

.chat-message .avatar img {
    max-width: 64px; /* Reduced size for a sleeker look */
    max-height: 64px;
    border-radius: 50%;
    object-fit: cover;
}

.chat-message .message {
    width: 85%;
    padding: 0 0.75rem;
    color: #d1d5db;
    font-size: 1rem;
    line-height: 1.5;
    word-wrap: break-word;
    margin-top: 0; /* Ensures the message starts from the top */
}

.stAppViewMain {
    background-image: url('https://i.ibb.co/kJrThG4/essai-bg-ZZZZZZ.jpg'); /* Replace with your image URL */
    background-size: cover; /* Ensures the image covers the entire section */
    background-position: center; /* Centers the background image */
    background-repeat: no-repeat; /* Prevents the image from repeating */
    height: 105vh; /* Optional: Ensures the background spans the full viewport height */
    width: 100%;
    overflow-y: auto; /* Allows vertical scrolling if content exceeds the view */
    overflow-x: hidden; /* Prevents horizontal overflow */
}






/* Additional styling for better aesthetics */
body {
    background-color: #202123;
    font-family: Arial, sans-serif;
    color: #d1d5db;
}

</style>

'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/LNMtCBz/475063-1.png" alt="bot avatar">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/fNVY5KK/monta-round.png" alt="user avatar">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''