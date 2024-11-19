css = '''
<style>
body {
    background-color: #f0f2f5;
    font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.chat-message {
    padding: 1rem; 
    border-radius: 0.75rem; 
    margin-bottom: 1rem; 
    display: flex;
    align-items: center;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    max-width: 85%;
    margin-left: auto;
    margin-right: auto;
}

.chat-message.user {
    background-color: #e6f2ff;
    align-self: flex-end;
    margin-left: auto;
    color: #2c3e50;
    justify-content: flex-end;
}

.chat-message.bot {
    background-color: #ffffff;
    align-self: flex-start;
    color: #2c3e50;
    border: 1px solid #e1e4e8;
}

.chat-message .avatar {
    width: 15%;
    margin: 0 1rem;
}

.chat-message .avatar img {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #e1e4e8;
}

.chat-message .message {
    width: 85%;
    font-size: 1rem;
    line-height: 1.6;
    font-weight: 400;
}

.chat-message.user .message {
    text-align: right;
    margin-right: 1rem;
}

.subheading {
    font-size: 24px;
    font-weight: bold;
    color: #ffffff; /* White text */
    background-color: #2c3e50; /* Dark blue-gray background */
    padding: 10px;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* Stronger shadow */
    margin-bottom: 20px;
}

.top-heading-container {
    background-color: #f0f4f8; /* Light grayish-blue background */
    color: #2c3e50; /* Darker text color */
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* Subtle shadow */
    margin-bottom: 30px;
}

.top-heading {
    font-size: 34px;
    font-weight: bold;
    margin: 0;
    color: #34495e; /* Slightly darker text for the heading */
}

.top-subheading {
    font-size: 18px;
    font-weight: lighter;
    color: #576574; /* Muted blue-gray text for the subheading */
    margin-top: 5px;
}

/style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/4MqZyxB/Screenshot-2024-11-13-202250.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="message">{{MSG}}</div>
    <div class="avatar">
        <img src="https://i.ibb.co/0fXttqr/Screenshot-2024-11-14-202351.png">
    </div>    
</div>
'''