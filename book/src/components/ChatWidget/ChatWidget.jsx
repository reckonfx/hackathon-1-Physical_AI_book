import React, { useState, useRef, useEffect } from 'react';
import clsx from 'clsx';
import styles from './ChatWidget.module.css';
import API_CONFIG from '../../utils/apiConfig';

const ChatWidget = ({ initialMessages = [] }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm your Physical AI & Robotics assistant. Ask me anything about ROS2, Gazebo, Isaac Sim, or VLA models!",
      sender: 'bot',
      timestamp: new Date().toLocaleTimeString()
    },
    ...initialMessages
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString()
    };

    // Add user message to chat
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call the backend RAG API
      const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.CHAT}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: [
            ...messages.filter(m => m.sender === 'user' || m.sender === 'assistant').map(m => ({
              role: m.sender === 'user' ? 'user' : 'assistant',
              content: m.text
            })),
            { role: 'user', content: inputValue }
          ]
        })
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();

      const botMessage = {
        id: Date.now() + 1,
        text: data.response,
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString(),
        sources: data.sources || []
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      const errorMessage = {
        id: Date.now() + 1,
        text: "Sorry, I encountered an error processing your request. Please try again.",
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (!isOpen && inputRef.current) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  };

  if (!isOpen) {
    return (
      <button className={clsx(styles.chatButton, styles.chatButtonFloat)} onClick={toggleChat}>
        <span className={styles.chatIcon}>💬</span>
        AI Assistant
      </button>
    );
  }

  return (
    <div className={styles.chatContainer}>
      <div className={styles.chatHeader}>
        <div className={styles.chatHeaderContent}>
          <h4>Physical AI Assistant</h4>
          <button className={styles.closeButton} onClick={toggleChat} aria-label="Close chat">
            ×
          </button>
        </div>
      </div>

      <div className={styles.chatMessages}>
        {messages.map((message) => (
          <div
            key={message.id}
            className={clsx(
              styles.message,
              styles[`${message.sender}Message`]
            )}
          >
            <div className={styles.messageContent}>
              <div className={styles.messageText}>{message.text}</div>
              {message.sources && message.sources.length > 0 && (
                <div className={styles.sources}>
                  <small>Sources: {message.sources.slice(0, 2).join(', ')}</small>
                </div>
              )}
              <div className={styles.messageTime}>{message.timestamp}</div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className={clsx(styles.message, styles.botMessage)}>
            <div className={styles.messageContent}>
              <div className={styles.typingIndicator}>
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className={styles.chatInputArea}>
        <textarea
          ref={inputRef}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask about ROS2, Isaac Sim, Gazebo, VLA models..."
          className={styles.chatInput}
          rows="1"
          disabled={isLoading}
        />
        <button
          onClick={handleSendMessage}
          disabled={!inputValue.trim() || isLoading}
          className={clsx(
            styles.sendButton,
            (!inputValue.trim() || isLoading) && styles.sendButtonDisabled
          )}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatWidget;