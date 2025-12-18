import React, { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await fetch('http://localhost:8000/travel/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
      });

      if (!res.ok) {
        const error = await res.json();
        setResponse({ error: error.detail || 'Failed to get recommendation.' });
        setLoading(false);
        return;
      }

      const data = await res.json();
      setResponse(data);
    } catch (error) {
      setResponse({ error: 'Failed to connect to backend. Make sure the backend server is running at http://localhost:8000' });
    }

    setLoading(false);
  };

  return (
    <div className="App">
      <h1>Travel Window Finder</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Example: I want to travel to Chikmagalur, Coorg and Sakleshpur for 5 days. What are the best conditions?"
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Finding...' : 'Find Best Window'}
        </button>
      </form>
      {response && (
        <div className="response">
          {response.error ? (
            <p>{response.error}</p>
          ) : (
            <>
              <h2>Recommended Travel Window</h2>
              <p><strong>Destinations:</strong> {response.destinations.join(', ')}</p>
              <p><strong>Duration:</strong> {response.duration_days} days</p>
              <p><strong>Best Window:</strong> {response.best_window.start_date} to {response.best_window.end_date}</p>
              <p><strong>Score:</strong> {response.best_window.score}/10</p>
              <h3>Reasons:</h3>
              <ul>
                {response.best_window.reasons.map((reason, index) => (
                  <li key={index}>{reason}</li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
