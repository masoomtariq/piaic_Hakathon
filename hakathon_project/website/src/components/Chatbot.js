import React, { useState, useEffect } from 'react';
import styles from './Chatbot.module.css'; // Assuming you'll create this CSS module
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

function Chatbot() {
  const { siteConfig } = useDocusaurusContext();
  const chatbotBackendUrl = siteConfig.customFields.chatbotBackendUrl;

  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedText, setSelectedText] = useState('');

  useEffect(() => {
    const handleMouseUp = () => {
      const selection = window.getSelection();
      if (selection) {
        setSelectedText(selection.toString().trim());
      }
    };

    document.addEventListener('mouseup', handleMouseUp);

    return () => {
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, []);

  const handleQueryChange = (event) => {
    setQuery(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!query.trim()) {
      setError('Please enter a query.');
      return;
    }

    setLoading(true);
    setError('');
    setResponse('');

    try {
      const res = await fetch(`${chatbotBackendUrl}/rag/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_query: query,
          collection_name: 'book_content', // This should match your Qdrant collection name
          selected_text: selectedText, // Send selected text for context
        }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || 'Failed to fetch response from chatbot backend.');
      }

      const data = await res.json();
      setResponse(data.response);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.chatbotContainer}>
      <h3>Textbook Chatbot</h3>
      {selectedText && (
        <div className={styles.selectedTextIndicator}>
          Context: "{selectedText}"
        </div>
      )}
      <form onSubmit={handleSubmit} className={styles.chatForm}>
        <input
          type="text"
          value={query}
          onChange={handleQueryChange}
          placeholder="Ask a question about the textbook..."
          className={styles.chatInput}
          disabled={loading}
        />
        <button type="submit" className={styles.chatButton} disabled={loading}>
          {loading ? (
            <>
              Thinking... <span className={styles.loadingSpinner}></span>
            </>
          ) : (
            'Ask'
          )}
        </button>
      </form>
      {error && <p className={styles.errorMessage}>{error}</p>}
      {response && (
        <div className={styles.chatResponse}>
          <h4>Response:</h4>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}

export default Chatbot;
