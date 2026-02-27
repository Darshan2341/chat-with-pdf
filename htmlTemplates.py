css = """
<style>
.chat-message {
    padding: 1.2rem;
    border-radius: 0.8rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
}
.chat-message.user {
    background-color: #2b313e;
}
.chat-message.bot {
    background-color: #475063;
}
.chat-message .avatar {
    font-size: 1.8rem;
    min-width: 40px;
    text-align: center;
}
.chat-message .message {
    color: #fff;
    font-size: 0.95rem;
    line-height: 1.5;
}
</style>
"""

user_template = """
<div class="chat-message user">
    <div class="avatar">🧑</div>
    <div class="message">{{MSG}}</div>
</div>
"""

bot_template = """
<div class="chat-message bot">
    <div class="avatar">🤖</div>
    <div class="message">{{MSG}}</div>
</div>
"""
