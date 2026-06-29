import React, { useState, useEffect } from 'react';

function App() {
  const [questions, setQuestions] = useState([]);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [results, setResults] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/questions?count=5')
      .then(res => res.json())
      .then(data => {
        setQuestions(data.questions || []);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  const handleAnswer = (questionId, answer) => {
    setSelectedAnswers({ ...selectedAnswers, [questionId]: answer });
    fetch('/api/answer', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question_id: questionId, answer })
    })
      .then(res => res.json())
      .then(data => setResults({ ...results, [questionId]: data }))
      .catch(console.error);
  };

  if (loading) return <div>Loading trivia questions...</div>;

  return (
    <div style={{ maxWidth: 800, margin: '0 auto', padding: 20 }}>
      <h1>Trivia Game</h1>
      {questions.map(q => (
        <div key={q.id} style={{ border: '1px solid #ccc', padding: 15, marginBottom: 15, borderRadius: 8 }}>
          <h3>{q.question}</h3>
          <p><small>Category: {q.category}</small></p>
          <div>
            {q.options.map(opt => (
              <button
                key={opt}
                onClick={() => handleAnswer(q.id, opt)}
                style={{
                  margin: 5,
                  padding: '8px 16px',
                  background: results[q.id]?.correct === true ? '#4CAF50' :
                              results[q.id]?.correct === false ? '#f44336' :
                              selectedAnswers[q.id] === opt ? '#2196F3' : '#eee',
                  color: results[q.id] ? 'white' : 'black',
                  border: 'none',
                  borderRadius: 4,
                  cursor: 'pointer'
                }}
                disabled={!!results[q.id]}
              >
                {opt}
              </button>
            ))}
          </div>
          {results[q.id] && (
            <div style={{ marginTop: 10 }}>
              {results[q.id].correct ? '✅ Correct!' : '❌ Wrong!'}
              <span style={{ marginLeft: 10 }}>
                Answer: {results[q.id].correct_answer}
              </span>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

export default App;