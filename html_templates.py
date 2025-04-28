css = '''
<style>
body {
    font-family: Arial, sans-serif;
    background-color: #1e1e1e;
    color: #fff;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.chat-container {
    width: 100%;
    max-width: 600px;
    background-color: #2b2b2b;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}

.chat-message {
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
}

.chat-message.user {
    background-color: #2b313e;
}

.chat-message.bot {
    background-color: #475063;
}

.chat-message .avatar {
    width: 10%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.chat-message .message {
    width: 90%;
    padding: 0 1rem;
    color: #fff;
}

.chat-input {
    width: 100%;
    padding: 1rem;
    border: none;
    border-top: 1px solid #444;
    background-color: #2b2b2b;
    color: #fff;
    font-size: 1rem;
    outline: none;
}

.chat-input::placeholder {
    color: #888;
}
</style>

'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        🤖
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        🧑
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''