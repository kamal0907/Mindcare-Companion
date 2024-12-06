import React, { useState } from 'react';
import './Chatbot.css';

const Chatbot = () => {
    // State variables to store user input and chat history
    const [userMessage, setUserMessage] = useState('');
    const [chatHistory, setChatHistory] = useState([]);

    // Function to fetch the chatbot response from the API
    const fetchChatbotResponse = async () => {
        if (userMessage.trim() === '') return;

        const newChatHistory = [...chatHistory, { sender: 'user', text: userMessage }];

        try {
            const response = await fetch('http://127.0.0.1:5000/chatbot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userMessage }),
            });

            const data = await response.json();
            newChatHistory.push({ sender: 'bot', text: data.response });
            setChatHistory(newChatHistory);
        } catch (error) {
            newChatHistory.push({ sender: 'bot', text: 'Sorry, I am having trouble connecting. Please try again later.' });
            setChatHistory(newChatHistory);
            console.error('Error fetching chatbot response:', error);
        }

        setUserMessage('');
    };

    // Function to handle form submission
    const handleSubmit = (e) => {
        e.preventDefault();
        fetchChatbotResponse();
    };

    return (
        <div className="chatbot">
            <div className="chat-window">
                {chatHistory.map((message, index) => (
                    <div
                        key={index}
                        className={`message ${message.sender === 'user' ? 'user' : 'bot'}`}
                    >
                        {message.text}
                    </div>
                ))}
            </div>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Type your message..."
                    value={userMessage}
                    onChange={(e) => setUserMessage(e.target.value)}
                />
                <button type="submit">Send</button>
            </form>
        </div>
    );
};

export default Chatbot;
