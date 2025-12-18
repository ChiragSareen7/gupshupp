import React, { useState, useEffect, useRef } from 'react';
import './App.css';

const API_BASE = process.env.REACT_APP_API_URL || '';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [personalities, setPersonalities] = useState([]);
  const [currentPersonality, setCurrentPersonality] = useState('neutral');
  const [memory, setMemory] = useState(null);
  const [useMemory, setUseMemory] = useState(false);
  const [comparisons, setComparisons] = useState(null);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    loadPersonalities();
    addSystemMessage("Welcome! Start chatting to see how different personalities respond. Try extracting memory after a few messages!");
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadPersonalities = async () => {
    try {
      const url = API_BASE ? `${API_BASE}/.netlify/functions/personalities` : `/.netlify/functions/personalities`;
      const response = await fetch(url);
      const data = await response.json();
      setPersonalities(data.personalities);
    } catch (error) {
      console.error('Error loading personalities:', error);
    }
  };

  const addSystemMessage = (text) => {
    setMessages(prev => [...prev, { role: 'assistant', content: text, isSystem: true }]);
  };

  const addMessage = (role, content) => {
    setMessages(prev => [...prev, { role, content }]);
  };

  const sendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage = inputValue.trim();
    setInputValue('');
    
    // Create updated messages array with new user message
    const newUserMessage = { role: 'user', content: userMessage };
    const updatedMessages = [...messages, newUserMessage];
    
    // Update state with user message
    setMessages(updatedMessages);

    setLoading(true);
    try {
      // Filter out system messages for API call
      const messagesToSend = updatedMessages.filter(msg => !msg.isSystem);
      
      const url = API_BASE ? `${API_BASE}/.netlify/functions/generate_response` : `/.netlify/functions/generate_response`;
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: messagesToSend,
          personality: currentPersonality,
          use_memory: useMemory
        })
      });

      const data = await response.json();
      if (data.error) {
        addSystemMessage('Error: ' + data.error);
      } else {
        addMessage('assistant', data.response);
      }
    } catch (error) {
      addSystemMessage('Error: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const extractMemory = async () => {
    if (messages.length === 0) {
      addSystemMessage('Please send some messages first!');
      return;
    }

    setLoading(true);
    try {
      const url = API_BASE ? `${API_BASE}/.netlify/functions/extract_memory` : `/.netlify/functions/extract_memory`;
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: messages })
      });

      const data = await response.json();
      if (data.error) {
        addSystemMessage('Error: ' + data.error);
      } else {
        setMemory(data);
      }
    } catch (error) {
      addSystemMessage('Error: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const comparePersonalities = async () => {
    if (!inputValue.trim()) {
      addSystemMessage('Please enter a message to compare personalities!');
      return;
    }

    const userMessage = inputValue.trim();
    setInputValue('');
    setLoading(true);
    
    try {
      const url = API_BASE ? `${API_BASE}/.netlify/functions/compare_personalities` : `/.netlify/functions/compare_personalities`;
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: messages,
          user_message: userMessage,
          personalities: ['neutral', 'calm_mentor', 'witty_friend', 'therapist_style'],
          use_memory: useMemory
        })
      });

      if (!response.ok) {
        const errorText = await response.text();
        addSystemMessage(`Error ${response.status}: ${errorText}`);
        return;
      }

      const data = await response.json();
      
      if (data.error) {
        addSystemMessage('Error: ' + data.error);
      } else if (data.comparisons && Object.keys(data.comparisons).length > 0) {
        setComparisons(data.comparisons);
        addSystemMessage(`Comparing ${Object.keys(data.comparisons).length} personalities for: "${userMessage}"`);
      } else {
        addSystemMessage('Error: No comparisons received from server');
        console.error('Unexpected response:', data);
      }
    } catch (error) {
      addSystemMessage('Error: ' + error.message);
      console.error('Compare personalities error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <div className="header">
          <h1>Memory & Personality Engine</h1>
          <p>Memory Extraction & Personality Engine</p>
        </div>

        <div className="main-content">
          <div className="card chat-section">
            <h2>Chat Interface</h2>
            <div className="personality-selector">
              {personalities.map(p => (
                <button
                  key={p.key}
                  className={`personality-btn ${currentPersonality === p.key ? 'active' : ''}`}
                  onClick={() => setCurrentPersonality(p.key)}
                >
                  {p.name}
                </button>
              ))}
            </div>
            <div className="chat-messages" ref={messagesEndRef}>
              {messages.map((msg, idx) => (
                <div key={idx} className={`message ${msg.role} ${msg.isSystem ? 'system' : ''}`}>
                  <div className="message-label">
                    {msg.isSystem ? 'System' : msg.role === 'user' ? 'You' : 'Assistant'}
                  </div>
                  <div>{msg.content}</div>
                </div>
              ))}
              {loading && (
                <div className="message assistant">
                  <div className="loading">Thinking...</div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
            <div className="chat-input">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                placeholder="Type your message..."
                disabled={loading}
              />
              <button onClick={sendMessage} disabled={loading}>
                {loading ? 'Sending...' : 'Send'}
              </button>
            </div>
            <div className="action-buttons">
              <button className="btn btn-primary" onClick={extractMemory} disabled={loading}>
                Extract Memory
              </button>
              <button className="btn btn-secondary" onClick={comparePersonalities} disabled={loading}>
                Compare Personalities
              </button>
            </div>
            <div className="checkbox-group">
              <label>
                <input
                  type="checkbox"
                  checked={useMemory}
                  onChange={(e) => setUseMemory(e.target.checked)}
                />
                Use Memory for Personalization
              </label>
            </div>
          </div>

          <div className="card">
            <h2>Extracted Memory</h2>
            <div className="memory-display">
              {memory ? (
                <>
                  {memory.preferences && memory.preferences.length > 0 && (
                    <div className="memory-section">
                      <h3>Preferences</h3>
                      {memory.preferences.map((p, idx) => (
                        <div key={idx} className="memory-item">
                          <strong>{p.category}:</strong> {p.preference}<br />
                          <small>Confidence: {(p.confidence * 100).toFixed(0)}% | Evidence: "{p.evidence}"</small>
                        </div>
                      ))}
                    </div>
                  )}
                  {memory.emotional_patterns && memory.emotional_patterns.length > 0 && (
                    <div className="memory-section">
                      <h3>Emotional Patterns</h3>
                      {memory.emotional_patterns.map((e, idx) => (
                        <div key={idx} className="memory-item">
                          <strong>{e.emotion}</strong> ({e.frequency})<br />
                          <small>Triggers: {e.triggers.join(', ')}</small><br />
                          <small>Evidence: "{e.evidence}"</small>
                        </div>
                      ))}
                    </div>
                  )}
                  {memory.facts && memory.facts.length > 0 && (
                    <div className="memory-section">
                      <h3>Facts</h3>
                      {memory.facts.map((f, idx) => (
                        <div key={idx} className="memory-item">
                          <strong>[{f.importance.toUpperCase()}]</strong> {f.fact}<br />
                          <small>Category: {f.category} | Evidence: "{f.evidence}"</small>
                        </div>
                      ))}
                    </div>
                  )}
                  {memory.summary && (
                    <div className="memory-section">
                      <h3>Summary</h3>
                      <div className="memory-item">{memory.summary}</div>
                    </div>
                  )}
                </>
              ) : (
                <p style={{ color: '#999', textAlign: 'center', padding: '20px' }}>
                  Memory will appear here after extraction
                </p>
              )}
            </div>
          </div>
        </div>

        {comparisons && (
          <div className="card comparison-section">
            <h2>Personality Comparison</h2>
            <div className="comparison-grid">
              {Object.entries(comparisons).map(([key, comp]) => (
                <div key={key} className="comparison-card">
                  <h3>{comp.name}</h3>
                  <div className="response">{comp.response}</div>
                </div>
              ))}
            </div>
            <button className="btn btn-secondary" onClick={() => setComparisons(null)} style={{ marginTop: '20px' }}>
              Close Comparison
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;

